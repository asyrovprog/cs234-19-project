import math
from util import *
from recommender import *


class ClinicalDoseRecommender(Recommender):

    def recommend(self, features):
        """
        features = ["age", "height", "weight", "race_asian", "race_black",
                     "race_missing", "enzyme", "amiodarone", "male", "aspirin",
                     "smoker"]
        """
        prediction = 4.0376 \
                     - 0.2546 * features[0] \
                     + 0.0118 * features[1] \
                     + 0.0134 * features[2] \
                     - 0.6752 * features[3] \
                     + 0.4060 * features[4] \
                     + 0.0443 * features[5] \
                     + 1.2799 * features[6] \
                     - 0.5695 * features[8]

        return mg_to_dose(math.pow(prediction, 2))

