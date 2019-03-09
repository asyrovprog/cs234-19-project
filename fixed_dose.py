from recommender import *


class FixedDoseRecommender(Recommender):

    def get_features(self, patient):
        """
        Algorithm-specific feature processing
        Dummy function, the returned features are not used in recommend function at all.
        But this will help us distinguish features not used vs features is None (missing data)

        :param patient: patient data
        :return: feature vector for the given patient
        """
        return 1

    def recommend(self, features):
        """
        Recommend an action.

        returns:
            action: An integer representing the selected action.
            payoff: None
            conf_interval: None
        """
        return self.config.fixed_dose, None, None
