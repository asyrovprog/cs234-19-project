from recommender import *
from preprocess import *
from sklearn import tree
from plot_utils import *
import math
import logging

LABEL_SUCCESS = 0
LABEL_FAILED = 1


# References:
#  A Practical Method for Solving Contextual Bandit Problems Using Decision Trees:
#       https://arxiv.org/pdf/1706.04687.pdf
#
# For further improvements (of performance issue):
#  Extremely Fast Decision Tree:
#       https://arxiv.org/pdf/1802.08780.pdf
#
class TreeHeuristicRecommender(Recommender):

    def get_clinical_meds(self, patient):
        enzyme = 1 if patient.properties[TEGRETOL] is BinaryFeature.true or \
                      patient.properties[DILANTIN] is BinaryFeature.true or \
                      patient.properties[RIFAMPIN] is BinaryFeature.true or \
                      any(m in patient.properties[MEDICATIONS] for m in ["carbamazepine", "phenytoin", "rifampin",
                                                                         "rifampicin"]) \
            else 0

        amiodarone = 1 if patient.properties[CORDARONE] is BinaryFeature.true or \
                          "amiodarone" in patient.properties[MEDICATIONS] \
            else 0
        return [enzyme, amiodarone]

    def load_basic_features(self, patient):
        features = [patient.properties[AGE].value, patient.properties[HEIGHT], patient.properties[WEIGHT],
                    1 if patient.properties[RACE] is Race.asian else 0,
                    1 if patient.properties[RACE] is Race.black else 0,
                    1 if patient.properties[RACE] is Race.unknown else 0] + self.get_clinical_meds(patient)

        return features

    def get_clinical_features(self, patient):
        """
        Same features as for clinical dose algorithm (a.k.a. basic)
        """
        if self.feature_names is None:
            self.init__basic_feature_names()

        return np.array(self.load_basic_features(patient))

    def init__basic_feature_names(self):
        self.feature_names = [AGE, HEIGHT, WEIGHT, "Asian", "African", "Other", "Enzyme", "Amiodarone"]

    def get_extended_features(self, patient):
        """
        Extended set of features
        """
        f = list([patient.properties[AGE].value]) + self.get_clinical_meds(patient) # size: 3

        f.append(feature_scaling(BMI_MIN, BMI_MAX,
                                 get_bmi(patient.properties[HEIGHT], patient.properties[WEIGHT])))  # size: 1

        f += get_one_hot(patient.properties[GENDER])    # size: 3
        f += get_one_hot(patient.properties[VKORC1_1639])   # size: 4
        f += get_one_hot(patient.properties[ASPIRIN])   # size: 3
        f += get_one_hot(patient.properties[SMOKER])    # size: 3
        f += get_one_hot(patient.properties[IS_STABLE]) # size: 3

        return np.array(f)

    def get_features(self, patient):
        f = self.config.feature_set
        if f == "clinical":
            return self.get_clinical_features(patient)
        return self.get_extended_features(patient)

    def __init__(self, config):
        super().__init__(config)

        self.num_arms = self.config.num_arms
        self.action_trees = []

        self.feature_names = None

        self.S_0 = []           # default success count (usually 1 for each arm)
        self.F_0 = []           # default failure count (usually 1 for each arm)
        self.Dta_x = []         # for each arm: samples which were classified as best for the arm
        self.Dta_y = []         # for each arm: actual results (classification succeeded/failed)

        self.iter = -1
        self.iter_item_id = 0
        self.num_correct = 0

        self.plot_mean = []
        self.plot_variance = []
        self.prev_iter = 0
        self.Nt = [] # number of times arm was tried

        self.reset()

    def reset(self):
        # we could change this to preffer med dosage
        self.S_0 = [1 for _ in range(self.num_arms)]
        self.F_0 = [1 for _ in range(self.num_arms)]

        # keep features for each arm, so that we can update Desision Tree
        self.Dta_x = [[] for _ in range(self.num_arms)]
        self.Dta_y = [[] for _ in range(self.num_arms)]

        self.Nt = [0  for _ in range(self.num_arms)]

        # Decision Tree for each action. At each node we keep number of
        # successes and failures (so our label is binary)
        self.action_trees = [None for _ in range(self.num_arms)]

        self.iter += 1
        self.iter_item_id = 0
        self.num_correct = 0


    def estimate_arm(self, params, arm):
        """
        Sample beta distrubution. params is (F, S) for
        X_arm ~ Beta(S_0[arm] + S, F_0[arm] + F)
        """
        S = self.S_0[arm] + params[1] + 1
        F = self.F_0[arm] + params[0]
        res = np.random.beta(S, F)
        return res

    def query_distribution(self, a, x_t):
        """
        Return number of successes and failures for the passed  (x_t, a) context, which
        are used for Beta() parameters
        """
        theta_tree = self.action_trees[a]

        # if tree is empty then we return 0 counts for successes and failures
        if theta_tree is None:
            return 0, 0

        #
        # The following code looks quite hacky, but we could not find more elegant way
        # to extract number of successes and failures from node for the context out of
        # sklearn DecisionTreeClassifier
        #
        node_id = theta_tree.apply([x_t])[0]
        total_samples = theta_tree.tree_.n_node_samples[node_id]
        probs = theta_tree.predict_proba([x_t])[0]
        class_ids = {theta_tree.classes_[i]: i for i in range(len(theta_tree.classes_))}
        result = [int(round(p * total_samples)) for p in probs]

        # return counts of successes (S) and failures (F) for the context
        S = result[class_ids[LABEL_SUCCESS]] if LABEL_SUCCESS in class_ids else 0
        F = result[class_ids[LABEL_FAILED]] if LABEL_FAILED in class_ids else 0
        return F, S

    def recommend(self, patient, eval_results, iter, patient_idx):
        x_t = self.get_features(patient)
        # distrubutions for arms
        p_a = [self.query_distribution(a, x_t) for a in range(self.num_arms)]
        # choose argmax arm
        action = np.argmax([self.estimate_arm(p_a[a], a) for a in range(self.num_arms)])
        return action, None, None

    def _update_tree(self, arm):
        """
        Update Decision Tree with new data point.

        Note: We could not find implementation of dynamic Desition Tree in
        well known packages for python.

        There are some available implementations, but we did not have chance to
        adopt any due to project time constraints.

        Therefore using sklearn implementation (which is not dynamic). This
        unfortunately significantly slows down training, because we have to
        rebuild action tree on each update.
        """
        t = tree.DecisionTreeClassifier(min_samples_split=self.config.min_samples_split,
            min_samples_leaf=self.config.min_samples_leaf, max_leaf_nodes=self.config.max_leaf_nodes,
            criterion=self.config.criterion,max_depth=self.config.tree_depth)

        self.action_trees[arm] = t
        t.fit(self.Dta_x[arm], self.Dta_y[arm])
        self.Nt[arm] += 1

    def update(self, arm, x_t, reward):
        label = LABEL_SUCCESS if reward == CORRECT_DOSE_REWARD else LABEL_FAILED
        self.Dta_x[arm].append(x_t)
        self.Dta_y[arm].append(label)
        self._update_tree(arm)

        #
        # the following should ideally be moved to executor
        #
        self.num_correct += 1 if label == LABEL_SUCCESS else 0
        accuracy = 1 if label == LABEL_SUCCESS else 0

        if len(self.plot_mean) == self.iter_item_id:
            self.plot_mean.append(accuracy)
            self.plot_variance.append(0.0)
        else:
            n = self.iter + 1
            idx = self.iter_item_id
            prev_mu = self.plot_mean[idx]
            prev_s2 = self.plot_variance[idx]

            self.plot_mean[idx] = mean_update(prev_mu, n, accuracy)
            self.plot_variance[idx] = variance_update(prev_s2, n, prev_mu, accuracy)

        self.iter_item_id += 1

    def plot(self):
        fill_plot(self.plot_mean, self.config.output_path + self.config.algo_name + "-accuracy.png", self.config.algo_name)

        if not self.feature_names is None:
            for a in range(self.num_arms):
                tree.export_graphviz(self.action_trees[a],
                    filled=True,
                    out_file=self.config.output_path + "tree_arm_" + str(a) + ".dot",
                    feature_names=self.feature_names)
