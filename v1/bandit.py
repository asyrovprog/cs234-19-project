import numpy as np


class ContextualBandit(object):
    """Base class for contextual bandit."""
    def update(self, arm, context_feature, reward):
        """Observe the reward.

        Observe the reward for a past action. Update parameters accordingly.

        Args:
            arm: the previous arm recommended by the bandit.
            context_feature: the feature used to compute the previous recommend arm.
            reward: the reward corresponding to the previous action.
        """
        pass

    def recommend(self, context_feature):
        """Recommend an action.

        Args:
            context_feature: a numpy array represents the input feature.
        Returns:
            An integer represents the selected action.
        """
        pass

    def reset(self):
        """Resets parameters."""
        pass


class FixDose(ContextualBandit):
    """Fix dose bandit."""
    def __init__(self, dose):
        self.dose = dose

    def recommend(self, context_feature):
        return self.dose


class LinUCB(ContextualBandit):
    """Linear UCB with disjoint models.

    Blog post: http://john-maxwell.com/post/2017-03-17/
    Reference: Li, Lihong, Wei Chu, John Langford, and Robert E Schapire. 2010. 
    “A Contextual-Bandit Approach to Personalized News Article Recommendation.” 
    In Proceedings of the 19th International Conference on World Wide Web, 
    661–70. ACM.


    """
    def __init__(self, alpha, d, num_arms):
        """
        Args:
            alpha: regularization parameter.
            d: number of features
            num_arms: number of arms
        """
        self.alpha = alpha
        self.d = d
        self.num_arms = num_arms

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
        self.A[arm] += context_feature @ np.transpose(context_feature)
        self.b[arm] += reward * context_feature

    def recommend(self, context_feature):
        payoff = {}
        for a in range(self.num_arms):
            self.theta[a] = np.linalg.inv(self.A[a]) @ self.b[a]
            payoff[a] = (np.transpose(self.theta[a]) @ context_feature +
                self.alpha * np.sqrt(np.transpose(context_feature) @ np.linalg.inv(self.A[a]) @ context_feature))

        best_arm = None
        best_payoff = -float('inf')
        for a, p in payoff.items():
            if best_arm is None:
                best_arm = a
                best_payoff = p
            elif p > best_payoff:
                best_arm = a
                best_payoff = p
                continue
            elif p == best_payoff and np.random.random_sample() < 0.5:
                # randomly break tie
                best_arm = a
                best_payoff = p
                continue
        return best_arm


if __name__ == "__main__":
    import evaluation
    import tools
    import pandas as pd

    # features, labels = tools.load_dataset_bandit(features_to_include=[
    #     "Height (cm)",
    #     "Weight (kg)",
    #     "Gender",
    #     "Race",
    #     "Ethnicity",
    #     "Age",
    #     "Rifampin or Rifampicin",
    #     "Carbamazepine (Tegretol)",
    #     "Phenytoin (Dilantin)",
    #     "Amiodarone (Cordarone)"
    # ])

    data = pd.DataFrame(tools.load_dataset_clinical())
    labels = data["label"].values
    features = data.loc[:,data.columns != "label"].values

    fix_dose = FixDose(tools.DOSE_MED)

    lin_ucb = LinUCB(
        alpha=1.0,
        d=features.shape[1],
        num_arms=3
    )
    regret, incorrect_frac = evaluation.evaluate(features, labels, fix_dose, 10)
    print("Fix dose regret: ", regret, " incorrect frac: ", incorrect_frac)
    regret, incorrect_frac = evaluation.evaluate(features, labels, lin_ucb, 10, verbose=True)
    print("LinUCB regret: ", regret, " incorrect frac: ", incorrect_frac)