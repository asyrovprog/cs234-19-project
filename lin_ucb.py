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

        # History reward
        # action -> num_observation
        self.c = {}

        # Learned params
        # action -> d
        self.theta = {}
        self.b = {}

        # Initialization
        for a in range(self.num_arms):
            self.A[a] = np.identity(self.d)
            self.b[a] = np.zeros(self.d)

    def update(self, arm, context_feature, reward):
        self.A[arm] += context_feature @ np.transpose(context_feature)
        self.b[arm] += reward * context_feature

    def recommend(self, context_feature):
        payoff = {}
        for a in range(self.num_arms):
            self.theta[a] = np.linalg.inv(self.A[a]) @ self.b[a]
            payoff[a] = (np.transpose(context_feature) @ self.theta[a] +
                self.alpha * np.sqrt(np.transpose(context_feature) @ np.linalg.inv(self.A[a]) @ context_feature))

        best_arm = None
        best_payoff = -float('inf')
        for a, p in payoff.items():
            if best_arm is None:
                best_arm = a
                best_payoff = p
                continue
            if p > best_payoff:
                best_arm = a
                best_payoff = p
                continue
            if p == best_payoff and np.random.random() < 0.5:
                # randomly break tie
                best_arm = a
                best_payoff = p
                continue
        return best_arm

