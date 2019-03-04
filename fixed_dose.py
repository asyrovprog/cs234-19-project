from recommender import *


class FixedDoseRecommender(Recommender):

    def recommend(self, features):
        """
        Recommend an action.

        returns:
            action: An integer representing the selected action.
            payoff: A float representing the estimated payoff of the selected action.
            conf_interval: A float representing the confidence interval for the estimated payoff
                            of the selected action.
        """
        return self.config.fixed_dose, None, None
