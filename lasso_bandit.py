from recommender import *
from preprocess import *
from sklearn.linear_model import Lasso
from collections import defaultdict


class LassoBandit(Recommender):
    """
    Implementation of Lasso bandit.

    Reference: http://web.stanford.edu/~bayati/papers/lassoBandit.pdf

    """

    def __init__(self, config):
        """
        Args:
            q: foced sampling parameter.
            h: localization parameter.
            lambda1: regularization parameter.
            lambda2: regularization parameter.
        """
        super().__init__(config)
        self.num_arms = self.config.num_arms

        # Forced sample hparam. Controls how frequently we force sample.
        self.q = self.config.q
        # Forced sample hparam. Controls how many force sample we generate. A very large
        # number would generally suffice.
        self.n = self.config.n

        # Confidence param. We first use the force sample model to select a subset of arms
        # based on this parameter. In practice we set this to a high number so that all arms
        # are included because we only have 3 arms.
        self.h = self.config.h
        self.init_lambda1 = self.config.lambda1
        self.init_lambda2 = self.config.lambda2

        self.reset()

    def reset(self):
        logging.debug(f"[{self.config.algo_name}] reset!")

        # Keep tract of iteration time. This is used to schedule forced arm sampling.
        self.t = 0

        # Arm -> Lasso estimator trained on forced samples.
        self.force_estimators = {}

        # Arm -> Lasso estimator trained on all samples.
        self.all_estimators = {}

        # Arm -> iteration where we should force sample an arm.
        self.force_sample_iter = defaultdict(set)

        # Keeps track of past data
        self.force_sample_X = defaultdict(list)
        self.force_sample_y = defaultdict(list)
        self.all_sample_X = defaultdict(list)
        self.all_sample_y = defaultdict(list)

        # Whether the previous prediction was forced.
        self.forced = False

        # Regularization.
        self.lambda1 = self.init_lambda1
        self.lambda2 = self.init_lambda2

        # Initialize force sample schedule.
        for a in range(self.num_arms):
            K = self.num_arms
            q = self.q
            # In the paper the arm starts from 1.
            i = a + 1
            for j in range(q * (i - 1) + 1, q * i + 1):
                for n in range(self.n):
                    self.force_sample_iter[a].add((2 ** n - 1) * K * q + j)

    def _train(self, lam, X, y):
        lasso = Lasso(alpha=lam,)
        lasso.fit(X, y)
        return lasso

    def get_features(self, patient):
        """
        Algorithm-specific feature processing

        :param patient: patient data
        :return: feature vector for the given patient
        """

        features = list([1, patient.properties[AGE].value])   # size 2

        # features += [patient.properties[f] for f in NUMERICAL_FEATURES]     # size 4
        # features.append(get_bmi(patient.properties[HEIGHT], patient.properties[WEIGHT]))    # size 1
        features.append(feature_scaling(BMI_MIN, BMI_MAX, get_bmi(patient.properties[HEIGHT],
                                                                  patient.properties[WEIGHT])))   # size 1
        # features.append(feature_scaling(HEIGHT_MIN, HEIGHT_MAX, patient.properties[HEIGHT]))    # size 1
        # features.append(feature_scaling(WEIGHT_MIN, WEIGHT_MAX, patient.properties[WEIGHT]))    # size 1
        features.append(feature_scaling(INR_MIN, INR_MAX, patient.properties[INR]))    # size 1
        features.append(feature_scaling(INR_MIN, INR_MAX, patient.properties[TARGET_INR]))    # size 1

        features += get_one_hot_from_list(patient.properties[INDICATION])   # size: 9

        features += get_one_hot(patient.properties[GENDER])  # size: 3
        features += get_one_hot(patient.properties[RACE])  # size: 5

        for f in BINARY_FEATURES:
            features += get_one_hot(patient.properties[f]) # size: 23 * 3 = 69

        features += get_one_hot_from_list(patient.properties[CYP2C9]) # size: 15

        for f in VKORC1_GENO_FEATURES:
            features += get_one_hot(patient.properties[f]) # size: 7 * 4 = 28

        return np.array(features)

    def update(self, arm, context_feature, reward):
        logging.debug(
            f"[{self.config.algo_name}] update: action={arm}; reward={reward}; context={context_feature}")
        if self.forced:
            self.force_sample_X[arm].append(context_feature)
            self.force_sample_y[arm].append(reward)
            self.force_estimators[arm] = self._train(
                self.lambda1,
                self.force_sample_X[arm],
                self.force_sample_y[arm]
            )

        self.all_sample_X[arm].append(context_feature)
        self.all_sample_y[arm].append(reward)
        self.lambda2 = self.init_lambda2 * np.sqrt(
            (np.log(self.t) + np.log(len(context_feature))) / self.t)

        self.all_estimators[arm] = self._train(
                self.lambda2,
                self.all_sample_X[arm],
                self.all_sample_y[arm]
            )

    def _get_force_arm(self, t):
        for a in range(self.num_arms):
            if t in self.force_sample_iter[a]:
                return a
        return None

    def _get_potential_arms(self, features):
        potential_arms = []
        predictions = []
        for a in range(self.num_arms):
            predictions.append(self.force_estimators[a].predict([features])[0])

        max_pred = np.max(predictions)
        for a, pred in enumerate(predictions):
            if pred >= max_pred - self.h:
                potential_arms.append(a)
        return potential_arms

    def _get_best_arm(self, potential_arms, features):
        max_pred = -float("inf")
        best_arm = -1

        for a in potential_arms:
            pred = self.all_estimators[a].predict([features])[0]
            if pred > max_pred:
                max_pred = pred
                best_arm = a
        return best_arm

    def recommend(self, patient, eval_results, iter, patient_idx):
        self.t += 1

        force_arm = self._get_force_arm(self.t)
        if force_arm is not None:
            self.forced = True
            return force_arm, None, None

        features = self.get_features(patient)
        potential_arms = self._get_potential_arms(features)
        # print("potential arms:", potential_arms)

        self.forced = False
        return self._get_best_arm(potential_arms, features), None, None
