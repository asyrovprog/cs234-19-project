import math
import numpy as np
from util import *
from recommender import *


class ClinicalDoseRecommender(Recommender):

    def get_features(self, patient):
        """
        Algorithm-specific feature processing

        :param patient: patient data
        :return: feature vector for the given patient
        """
        features = [1, patient.properties[AGE]]
        return features

    def recommend(self, patient):
        """
        Recommend an action.

        :param patient: patient data
        :return:
            action: An integer representing the selected action.
            payoff: None
            conf_interval: None
        """
        weights = [4.0376, -0.2546, 0.0118, 0.0134, -0.6752, 0.4060, 0.0443, 1.2799, -0.5695]

        features = self.get_features(patient)

        dose = np.dot(weights, features)

        return mg_to_dose(math.pow(dose, 2)), None, None

