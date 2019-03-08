from recommender import *


class FixedDoseRecommender(Recommender):

    def recommend(self, features):
        """
        Recommend an action.

        returns:
            action: An integer representing the selected action.
            payoff: None
            conf_interval: None
        """
        return self.config.fixed_dose, None, None
