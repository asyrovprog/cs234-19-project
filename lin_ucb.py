import numpy as np
from recommender import *
from feature import *
from constant import *


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
        self.logger.debug(f"[{self.config.algo_name}] reset!")
        for a in range(self.num_arms):
            self.A[a] = np.identity(self.d)
            self.b[a] = np.zeros(self.d)

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

    def update(self, arm, context_feature, reward):
        self.logger.debug(f"[{self.config.algo_name}] update: action={arm}; reward={reward}; context={context_feature}")
        self.A[arm] += context_feature @ context_feature.T
        self.b[arm] += (reward * context_feature)

    def recommend(self, patient):
        payoff = {}
        best_arm = None
        best_payoff = -float('inf')
        best_conf_interval = None

        context_feature = self.get_features(patient)

        for a in range(self.num_arms):
            self.theta[a] = np.linalg.inv(self.A[a]) @ self.b[a]
            conf_interval = self.alpha * np.sqrt(context_feature.T @ np.linalg.inv(self.A[a])
                                                 @ context_feature)
            payoff[a] = (self.theta[a].T @ context_feature) + conf_interval

            if payoff[a] > best_payoff:
                best_payoff = payoff[a]
                best_arm = a
                best_conf_interval = conf_interval

        self.logger.debug(f"[{self.config.algo_name}] recommend: chosen action={best_arm}; "
                          f"estimated payoff={best_payoff}; conf interval={best_conf_interval}")

        return best_arm, best_payoff, best_conf_interval

