import math
import logging
import numpy as np
from recommender import *
from feature import *
from preprocess import *


class ClinicalDoseRecommender(Recommender):

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

    def recommend(self, patient, eval_results, iter, patient_idx):
        """
        Recommend an action.

        :param patient: patient data
        :return:
            action: An integer representing the selected action.
            payoff: None
            conf_interval: None
        """
        weights = np.array([4.0376, -0.2546, 0.0118, 0.0134, -0.6752, 0.4060, 0.0443, 1.2799, -0.5695])
        features = self.get_features(patient)
        if features is None:
            return None, None, None
        dose = np.dot(weights, features)
        return parse_dose(math.pow(dose, 2)), None, None


