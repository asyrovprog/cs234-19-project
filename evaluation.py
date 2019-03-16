# Utility functions for evaluation.
import numpy as np
import math
from config import *
from util import *
import time

class EvalResults:
    """
    Class for encapsulating evaluation results
    """
    def __init__(self, is_training, models, num_iter=1):
        """
        Initialize EvalResults Class

        """
        self.is_training = is_training
        self.models = models
        self.regrets = [[[]for i in range(num_iter)] for j in range(len(models))]
        self.mistakes = [[[] for i in range(num_iter)] for j in range(len(models))]
        self.payoffs = [[[]for i in range(num_iter)] for j in range(len(models))]
        self.conf_intervals = [[[]for i in range(num_iter)] for j in range(len(models))]

    def log_results(self, model_idx, iter_idx, regrets, mistakes, payoffs, conf_intervals):
        self.regrets[model_idx][iter_idx] = regrets
        self.mistakes[model_idx][iter_idx] = mistakes
        self.payoffs[model_idx][iter_idx] = payoffs
        self.conf_intervals[model_idx][iter_idx] = conf_intervals

    def export_results(self):
        for m in range(len(self.models)):
            model_config = self.models[m].config
            export_stats_list(self.regrets[m],
                              model_config.get_regret_filename(model_config.algo_name, self.is_training))
            export_stats_list(self.mistakes[m],
                              model_config.get_mistake_filename(model_config.algo_name, self.is_training))
            if self.payoffs[m][0] is not None and len(self.payoffs[m][0]) > 0:
                export_stats_list(self.payoffs[m],
                                  model_config.get_payoff_filename(model_config.algo_name, self.is_training))
            if self.conf_intervals[m][0] is not None and len(self.conf_intervals[m][0]) > 0:
                export_stats_list(self.conf_intervals[m],
                                  model_config.get_conf_interval_filename(model_config.algo_name, self.is_training))

    def get_per_iter_mean_regret_for_model(self, model_idx, iter_idx):
        """
        Returns mean regret for the given model across the given iteration

        :param model_idx: index of the model
        :param iter_idx: index of the iteration
        :return: mean regret for the given model across the given iteration
        """
        if self.regrets is None or model_idx < 0 or model_idx >= len(self.regrets) \
                or iter_idx < 0 or iter_idx >= len(self.regrets[0]):
            return None

        return np.mean(self.regrets[model_idx][iter_idx])

    def get_overall_mean_regret_for_model(self, model_idx):
        """
         Returns mean regret for the given model across all iterations

         :param model_idx: index of the model
         :return: mean regret for the given model across all iterations
         """
        if self.regrets is None or model_idx < 0 or model_idx >= len(self.regrets):
            return None

        return np.mean([self.get_per_iter_mean_regret_for_model(model_idx, i)
                        for i in range(len(self.regrets[model_idx]))])

    def get_per_iter_err_rate_for_model(self, model_idx, iter_idx):
        """
        Returns error rate for the given model across the given iteration

        :param model_idx: index of the model
        :param iter_idx: index of the iteration
        :return: error rate for the given model across the given iteration
        """
        if self.mistakes is None or model_idx < 0 or model_idx >= len(self.mistakes) \
                or iter_idx < 0 or iter_idx >= len(self.mistakes[0]):
            return None

        return np.mean(self.mistakes[model_idx][iter_idx])

    def get_overall_err_rate_for_model(self, model_idx):
        """
        Returns error rate for the given model across all iterations

        :param model_idx: index of the model
        :return: error rate for the given model across all iterations
        """
        if self.mistakes is None or model_idx < 0 or model_idx >= len(self.mistakes):
            return None

        return np.mean([self.get_per_iter_err_rate_for_model(model_idx, i)
                        for i in range(len(self.mistakes[model_idx]))])


def shuffle_split_data_set(patients, trainset_ratio = 0.8):
    data_set_size = len(patients)
    training_set_size = math.ceil(data_set_size * trainset_ratio)
    indices = np.arange(data_set_size)
    np.random.shuffle(indices)
    training_indices = indices[:training_set_size]
    testing_indices = indices[training_set_size:]
    return training_indices, testing_indices


def run(patients, models, num_iter=1, trainset_ratio=0.8, verbose=False):

    np.random.seed(int(time.time()))

    if patients is None or len(patients) == 0 or models is None or len(models) == 0 \
            or num_iter < 1:
        return

    if trainset_ratio < 0: trainset_ratio = 0
    elif trainset_ratio > 1: trainset_ratio = 1

    # log all data for plotting
    training_results = EvalResults(True, models, num_iter) if trainset_ratio > 0 else None
    testing_results = EvalResults(False, models, num_iter) if trainset_ratio < 1 else None

    # perform N-fold validation based on the provided training/testing split
    # train the model on the training set then freeze the model to test on the testing set
    for i in range(num_iter):

        training_indices, testing_indices = shuffle_split_data_set(patients, trainset_ratio)

        for m in range(len(models)):

            model = models[m]
            model.reset()

            # training on the training set
            if trainset_ratio > 0:
                if verbose:
                    print(f"Training Iteration: {i}, model: {model.config.algo_name}")

                training_regrets, training_mistakes, training_payoffs, training_conf_intervals = \
                    model.run(patients, training_indices, is_training=True)
                # log training regret, estimated payoff & its confidence interval
                training_results.log_results(m, i, training_regrets, training_mistakes,
                                             training_payoffs, training_conf_intervals)

                if verbose:
                    print(f"mean regret: {training_results.get_per_iter_mean_regret_for_model(m, i)}, "
                          f"accuracy: {1 - training_results.get_per_iter_err_rate_for_model(m, i)}")

            # testing on the test set with the model params frozen
            if trainset_ratio < 1:
                if verbose:
                    print(f"Testing Iteration: {i}, model: {model.config.algo_name}")

                testing_regrest, testing_mistakes, testing_payoffs, testing_conf_intervals = \
                    model.run(patients, testing_indices, is_training=False)
                # log testing regret, estimated payoff & its confidence interval
                testing_results.log_results(m, i, testing_regrest, testing_mistakes,
                                            testing_payoffs, testing_conf_intervals)

                if verbose:
                    print(f"mean regret: {testing_results.get_per_iter_mean_regret_for_model(m, i)}, "
                          f"accuracy: {1 - testing_results.get_per_iter_err_rate_for_model(m, i)}")

    if trainset_ratio > 0:
        training_results.export_results()

    if trainset_ratio < 1:
        testing_results.export_results()

    if verbose:
        print("------------------------\n[SUMMARY OF THE RUN]")
        if trainset_ratio > 0:
            print(f"------------------------\nTraining: {trainset_ratio * 100}% patients")
            for m in range(len(models)):
                print(f"model: {models[m].config.algo_name}, "
                      f"mean regret: {training_results.get_overall_mean_regret_for_model(m)}, "
                      f"accuracy: {1 - training_results.get_overall_err_rate_for_model(m)}")
        if trainset_ratio < 1:
            print(f"------------------------\nTesting: {(1 - trainset_ratio) * 100}% patients")
            for m in range(len(models)):
                print(f"model: {models[m].config.algo_name}, "
                      f"mean regret: {testing_results.get_overall_mean_regret_for_model(m)}, "
                      f"accuracy: {1 - testing_results.get_overall_err_rate_for_model(m)}")

