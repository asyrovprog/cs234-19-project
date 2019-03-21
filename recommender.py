import logging
import numpy as np
from util import *


class Recommender(object):
    """
    Abstract Class for implementing a Dose Recommendation Algorithm
    """
    def __init__(self, config):
        """
        Initialize Recommender Class

        Args:
                config: class with hyperparameters
                logger: logger instance from the logging module
        """
        self.config = config

    def get_reward(self, action, label):
        return CORRECT_DOSE_REWARD if action == label else INCORRECT_DOSE_REWARD

    def get_features(self, patient):
        """
        Algorithm-specific feature processing

        :param patient: patient data
        :return: feature vector for the given patient
        """
        pass

    def reset(self):
        """
        Reset params.
        """
        pass

    def update(self, arm, context_feature, reward):
        """Observe the reward.

        Observe the reward for a past action. Update parameters accordingly.

        Args:
            arm: the previous arm recommended by the bandit.
            context_feature: the feature used to compute the previous recommend arm.
            reward: the reward corresponding to the previous action.
        """
        pass

    def recommend(self, patient, eval_results, iter, patient_idx):
        """
        Recommend an action.

        returns:
            action: An integer representing the selected action.
            payoff: A float representing the estimated payoff of the selected action.
            conf_interval: A float representing the confidence interval for the estimated payoff
                            of the selected action.
        """
        pass

    def run(self, patients, indices, eval_results, iter, is_training=False):
        """
        Run the model with the provided patient data set.
        When training mode is set to True, the model internal weights are updated.
        Otherwise, run the model in testing mode with no updates to the weights.

        :param patients: complete patient data set
        :param indices: indicies into the patient data set for data points
        :param is_training: whether to run the model in training mode (which updates weights)
        :return: lists of regrets and mistakes
        """
        regrets, mistakes = [], []
        actions, payoffs, conf_intervals = [], [], []
        risks = np.zeros((3, 3), dtype=int)  # keep track of decisions made

        for i in range(len(indices)):
            index = indices[i]
            patient = patients[index]
            features = self.get_features(patient)
            # skip insufficient records
            if features is None:
                continue
            # ground truth
            label = patient.properties[DOSE]

            action, payoff, conf_interval = self.recommend(patient, eval_results, iter, i)
            actions.append(action)
            reward = self.get_reward(action, label)

            # only updates the model params in training mode
            if is_training:
                self.update(action, features, reward)

            regret = self.get_reward(label, label) - reward
            regrets.append(regret)
            mistakes.append(0 if action == label else 1)
            risks[label][action] += 1

            if payoff is not None:
                payoffs.append(payoff)
            if conf_interval is not None:
                conf_intervals.append(conf_interval)

        return actions, regrets, mistakes, payoffs, conf_intervals, risks
