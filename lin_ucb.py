import numpy as np
from recommender import *


class LinUCBDisjointRecommender(Recommender):
    """
    Linear UCB with disjoint models.
    Blog post: http://john-maxwell.com/post/2017-03-17/
    Reference: Li, Lihong, Wei Chu, John Langford, and Robert E Schapire. 2010.
    “A Contextual-Bandit Approach to Personalized News Article Recommendation.”
    In Proceedings of the 19th International Conference on World Wide Web,
    661–70. ACM.
    """
    def __init__(self, config, d):
        """
        Args:
            alpha: regularization parameter.
            d: number of features
            num_arms: number of arms
        """
        super().__init__(config)
        self.alpha = self.config.alpha
        self.d = d
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
        for a in range(self.num_arms):
            self.A[a] = np.identity(self.d)
            self.b[a] = np.zeros(self.d)

    def update(self, arm, context_feature, reward):
        self.A[arm] += context_feature @ context_feature.T
        self.b[arm] += (reward * context_feature)

    def recommend(self, context_feature):
        payoff = {}
        best_arm = None
        best_payoff = -float('inf')
        best_conf_interval = None

        for a in range(self.num_arms):
            self.theta[a] = np.linalg.inv(self.A[a]) @ self.b[a]
            conf_interval = self.alpha * np.sqrt(context_feature.T @ np.linalg.inv(self.A[a])
                                                 @ context_feature)
            payoff[a] = (self.theta[a].T @ context_feature) + conf_interval

            if payoff[a] > best_payoff:
                best_payoff = payoff[a]
                best_arm = a

        return best_arm, best_payoff, best_conf_interval

