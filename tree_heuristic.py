from recommender import *
from preprocess import *
from sklearn import tree
from plot_utils import *

LABEL_SUCCESS = 0
LABEL_FAILED = 1

#
# References:
#  A Practical Method for Solving Contextual Bandit Problems Using Decision Trees:
#       https://arxiv.org/pdf/1706.04687.pdf
#
# For further improvements (of performance issue):
#  Extremely Fast Decision Tree:
#       https://arxiv.org/pdf/1802.08780.pdf
#
class TreeHeuristicRecommender(Recommender):

    def get_features0(self, patient):

        if patient.properties[AGE].value == AgeGroup.unknown or \
            patient.properties[HEIGHT] == VAL_UNKNOWN or \
            patient.properties[WEIGHT] == VAL_UNKNOWN or \
            patient.properties[DOSE] == VAL_UNKNOWN:
            return None

        enzyme = 1 if patient.properties[TEGRETOL] is BinaryFeature.true or \
                      patient.properties[DILANTIN] is BinaryFeature.true or \
                      patient.properties[RIFAMPIN] is BinaryFeature.true or \
                      any(m in patient.properties[MEDICATIONS] for m in ["carbamazepine", "phenytoin", "rifampin", "rifampicin"]) \
            else 0

        amiodarone = 1 if patient.properties[CORDARONE] is BinaryFeature.true or "amiodarone" in patient.properties[MEDICATIONS] \
            else 0

        features = [patient.properties[AGE].value, patient.properties[HEIGHT], patient.properties[WEIGHT],
                    1 if patient.properties[RACE] is Race.asian else 0,
                    1 if patient.properties[RACE] is Race.black else 0,
                    1 if patient.properties[RACE] is Race.unknown else 0,
                    enzyme, amiodarone]

        if self.feature_names is None:
            self.feature_names = [AGE, HEIGHT, WEIGHT, "Asia", "Africa", "Other", "Enzyme", "Amiodarone"]

        return np.array(features)

    def get_features1(self, patient):
        if patient.properties[AGE].value == AgeGroup.unknown or \
            patient.properties[HEIGHT] == VAL_UNKNOWN or \
            patient.properties[WEIGHT] == VAL_UNKNOWN or \
            patient.properties[DOSE] == VAL_UNKNOWN:
            return None

        features = [patient.properties[AGE].value, patient.properties[HEIGHT],
                    patient.properties[WEIGHT]]  # size: 3
        features += get_one_hot(patient.properties[GENDER])  # size: 3
        features += get_one_hot(patient.properties[RACE])  # size: 5
        features += get_one_hot(patient.properties[VKORC1_1639])  # size: 4

        if self.feature_names is None:
            self.feature_names = [AGE, HEIGHT, WEIGHT,
                                  "Gender[0]", "Gender[1]", "Gender[2]",
                                  "Race[0]", "Race[1]", "Race[2]", "Race[3]", "Race[4]",
                                  "VKORC1[0]", "VKORC1[1]", "VKORC1[2]", "VKORC1[3]"]

        return np.array(features)

    def get_features(self, patient):
        if self.config.alternative_features:
            return self.get_features1(patient)
        return self.get_features0(patient)

    def __init__(self, config):
        super().__init__(config)

        self.num_arms = self.config.num_arms
        self.action_trees = []

        self.feature_names = None

        self.S_0 = []           # default success count (usually 1 for each arm)
        self.F_0 = []           # default failure count (usually 1 for each arm)
        self.Dta_x = []         # for each arm: samples which were classified as best for the arm
        self.Dta_y = []         # for each arm: actual results (classification succeeded/failed)

        self.iter = 0
        self.iter_item_id = 0
        self.num_correct = 0

        self.plot_mean = []
        self.plot_variance = []
        self.prev_iter = 0

        self.reset()

    def reset(self):
        # we could change this to preffer med dosage
        self.S_0 = [1 for _ in range(self.num_arms)]
        self.F_0 = [1 for _ in range(self.num_arms)]

        # keep features for each arm, so that we can update Desision Tree
        self.Dta_x = [[] for _ in range(self.num_arms)]
        self.Dta_y = [[] for _ in range(self.num_arms)]

        # Decision Tree for each action. At each node we keep number of
        # successes and failures (so our label is binary)
        self.action_trees = [None for _ in range(self.num_arms)]

        self.iter = 0
        self.iter_item_id = 0
        self.num_correct = 0


    def sample_beta(self, params, arm):
        """
            Sample beta distrubution. params is (F, S) for
        X_arm ~ Beta(S_0[arm] + S, F_0[arm] + F)
        """
        S = self.S_0[arm] + params[1]
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

    def recommend(self, patient):
        x_t = self.get_features(patient)
        # distrubutions for arms
        p_a = [self.query_distribution(a, x_t) for a in range(self.num_arms)]
        # choose argmax arm
        action = np.argmax([self.sample_beta(p_a[a], a) for a in range(self.num_arms)])
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
        self.action_trees[arm] = tree.DecisionTreeClassifier(criterion = self.config.criterion, max_depth = self.config.tree_depth)
        self.action_trees[arm].fit(self.Dta_x[arm], self.Dta_y[arm])

    def update(self, arm, x_t, reward):
        label = LABEL_SUCCESS if reward == CORRECT_DOSE_REWARD else LABEL_FAILED
        self.Dta_x[arm].append(x_t)
        self.Dta_y[arm].append(label)
        self._update_tree(arm)

        #
        # the following should ideally be moved to executor
        #
        self.num_correct += 1 if label == LABEL_SUCCESS else 0
        accuracy = self.num_correct / (self.iter_item_id + 1)

        if len(self.plot_mean) == self.iter_item_id:
            self.plot_mean.append(accuracy)
            self.plot_variance.append(0.0)
        else:
            n, idx = self.iter + 1, self.iter_item_id
            prev_mu = self.plot_mean[idx]
            prev_s2 = self.plot_variance[idx]

            self.plot_mean[idx] = mean_update(prev_mu, n, accuracy)
            self.plot_variance[idx] = variance_update(prev_s2, n, prev_mu, accuracy)

        self.iter_item_id += 1

    def plot(self):
        for a in range(self.num_arms):
            tree.export_graphviz(self.action_trees[a],
                 filled=True,
                 out_file=self.config.output_path + "tree_arm_" + str(a) + ".dot",
                 feature_names=self.feature_names)
        fill_plot(self.plot_mean[20:], self.plot_variance[20:], self.config.output_path + "result.png", "DecisionTree-Beta")
