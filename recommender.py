import os
from util import *


class Recommender(object):
    """
    Abstract Class for implementing a Dose Recommendation Algorithm
    """
    def __init__(self, config, logger=None):
        """
        Initialize Recommender Class

        Args:
                config: class with hyperparameters
                logger: logger instance from the logging module
        """
        # directory for training outputs
        if not os.path.exists(config.output_path):
          os.makedirs(config.output_path)

        # store hyperparameters
        self.config = config
        self.logger = logger
        if logger is None:
          self.logger = get_logger(config.log_path)

    def update(self, arm, context_feature, reward):
        """Observe the reward.

        Observe the reward for a past action. Update parameters accordingly.

        Args:
            arm: the previous arm recommended by the bandit.
            context_feature: the feature used to compute the previous recommend arm.
            reward: the reward corresponding to the previous action.
        """
        pass

    def recommend(self, features):
        """
        Recommend an action.

        returns: An integer represents the selected action.
        """
        pass


