import numpy as np
import logging
from recommender import *
from feature import *
from constant import *
from preprocess import *


class LinUCBDisjointRecommender(Recommender):
    """
    Linear UCB with disjoint models.
    Blog post: http://john-maxwell.com/post/2017-03-17/
    Reference: Li, Lihong, Wei Chu, John Langford, and Robert E Schapire. 2010.
    “A Contextual-Bandit Approach to Personalized News Article Recommendation.”
    In Proceedings of the 19th International Conference on World Wide Web,
    661–70. ACM.
    """
    def __init__(self, config):
        """
        Args:
            alpha: regularization parameter.
            d: number of features
            num_arms: number of arms
        """
        super().__init__(config)
        self.alpha = self.config.alpha
        self.d = self.config.feature_count
        self.num_arms = len(self.config.actions)

        # Convenience variable.
        # A = D^T * D + I
        # where D is the num_observation * d design matrix
        # action -> d * d.
        self.A = {}

        # Learned params
        # action -> d
        self.theta = {}
        self.b = {}
        self.reset()

    def reset(self):
        logging.debug(f"[{self.config.algo_name}] reset!")
        for a in range(self.num_arms):
            self.A[a] = np.identity(self.d)               # d x d
            self.b[a] = np.atleast_2d(np.zeros(self.d)).T # d x 1

    def get_features(self, patient):
        """
        Algorithm-specific feature processing

        :param patient: patient data
        :return: feature vector for the given patient
        """
        # missing values, we can't apply the algorithm
        # if patient.properties[DOSE] == VAL_UNKNOWN or \
        #     patient.properties[AGE].value == AgeGroup.unknown or \
        #     patient.properties[HEIGHT] == VAL_UNKNOWN or \
        #     patient.properties[WEIGHT] == VAL_UNKNOWN:
        #     return None
        #
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
        logging.debug(f"[{self.config.algo_name}] update: action={arm}; reward={reward}; context={context_feature}")
        self.A[arm] += np.outer(context_feature, context_feature)
        self.b[arm] += reward * np.reshape(context_feature, (self.d, 1))

    def recommend(self, patient, eval_results, iter, patient_idx):
        payoff = {}
        best_arm = None
        best_payoff = -float('inf')
        best_conf_interval = None

        fvec = self.get_features(patient)
        if fvec is None:
            return None, None, None

        for a in range(self.num_arms):
            invA = np.linalg.inv(self.A[a])
            self.theta[a] = np.dot(invA, self.b[a])
            conf_interval = self.alpha * np.sqrt(np.dot(fvec.T, np.dot(invA, fvec)))

            payoff[a] = (np.dot(self.theta[a].T, fvec)) + conf_interval

            if payoff[a] > best_payoff:
                best_payoff = payoff[a]
                best_arm = a
                best_conf_interval = conf_interval

        logging.debug(f"[{self.config.algo_name}] recommend: chosen action={best_arm}; "
                          f"estimated payoff={best_payoff}; conf interval={best_conf_interval}")

        return best_arm, best_payoff, best_conf_interval


class LinUCBDisjointBasicRecommender(LinUCBDisjointRecommender):
    """
    Linear UCB with disjoint model using the same feature set as
    Clinical_Dose model
    """
    def __init__(self, config):
        """
        Args:
            alpha: regularization parameter.
            d: number of features
            num_arms: number of arms
        """
        super().__init__(config)
        self.alpha = self.config.alpha
        self.d = self.config.feature_count


    def get_features(self, patient):
        """
        Algorithm-specific feature processing

        :param patient: patient data
        :return: feature vector for the given patient
        """
        enzyme = 1 if patient.properties[TEGRETOL] is BinaryFeature.true or \
                      patient.properties[DILANTIN] is BinaryFeature.true or \
                      patient.properties[RIFAMPIN] is BinaryFeature.true or \
                      any(m in patient.properties[MEDICATIONS] for m in ["carbamazepine", "phenytoin", "rifampin",
                                                                         "rifampicin"]) \
                else 0

        amiodarone = 1 if patient.properties[CORDARONE] is BinaryFeature.true or \
                         "amiodarone" in patient.properties[MEDICATIONS] \
                    else 0

        features = [1, patient.properties[AGE].value, patient.properties[HEIGHT], patient.properties[WEIGHT],
                    1 if patient.properties[RACE] is Race.asian else 0,
                    1 if patient.properties[RACE] is Race.black else 0,
                    1 if patient.properties[RACE] is Race.unknown else 0,
                    enzyme, amiodarone]

        return np.array(features)

