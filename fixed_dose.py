from recommender import *


class FixedDoseRecommender(Recommender):

    def recommend(self, features):
        return self.config.fixed_dose
