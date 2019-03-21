# Utility functions for evaluation.
import numpy as np
import logging
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
        self.truths = [[]for i in range(num_iter)]
        self.actions = [[[]for i in range(num_iter)] for j in range(len(models))]
        self.regrets = [[[]for i in range(num_iter)] for j in range(len(models))]
        self.mistakes = [[[] for i in range(num_iter)] for j in range(len(models))]
        self.payoffs = [[[]for i in range(num_iter)] for j in range(len(models))]
        self.conf_intervals = [[[]for i in range(num_iter)] for j in range(len(models))]
        self.risks = [[[] for i in range(num_iter)] for j in range(len(models))]

    def log_truths(self, iter_idx, patients, indices):
        if len(self.truths[iter_idx]) == 0:
            self.truths[iter_idx] = [patients[i].properties[DOSE] for i in indices]

    def log_results(self, model_idx, iter_idx, actions, regrets, mistakes, payoffs, conf_intervals, risks):
        self.actions[model_idx][iter_idx] = actions
        self.regrets[model_idx][iter_idx] = regrets
        self.mistakes[model_idx][iter_idx] = mistakes
        self.payoffs[model_idx][iter_idx] = payoffs
        self.conf_intervals[model_idx][iter_idx] = conf_intervals
        self.risks[model_idx][iter_idx] = risks.flatten()

    def export_results(self):
        for m in range(len(self.models)):
            model_config = self.models[m].config
            if m == 0:
                export_stats_list(self.truths,
                                  model_config.get_truth_filename(self.is_training))
            export_stats_list(self.actions[m],
                              model_config.get_action_filename(model_config.algo_name, self.is_training))
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
            export_stats_list(self.risks[m],
                              model_config.get_risk_filename(model_config.algo_name, self.is_training))

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

    def get_per_iter_total_regret_for_model(self, model_idx, iter_idx):
        """
        Returns total regret for the given model across the given iteration

        :param model_idx: index of the model
        :param iter_idx: index of the iteration
        :return: total regret for the given model across the given iteration
        """
        if self.regrets is None or model_idx < 0 or model_idx >= len(self.regrets) \
                or iter_idx < 0 or iter_idx >= len(self.regrets[0]):
            return None

        return np.sum(self.regrets[model_idx][iter_idx])

    def get_avg_total_regret_for_model(self, model_idx):
        """
         Returns mean regret for the given model across all iterations

         :param model_idx: index of the model
         :return: mean regret for the given model across all iterations
         """
        if self.regrets is None or model_idx < 0 or model_idx >= len(self.regrets):
            return None

        return np.mean([self.get_per_iter_total_regret_for_model(model_idx, i)
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


def shuffle_split_data_set(patients, trainset_ratio=0.8):
    data_set_size = len(patients)
    training_set_size = math.ceil(data_set_size * trainset_ratio)
    indices = np.arange(data_set_size)
    np.random.shuffle(indices)
    training_indices = indices[:training_set_size]
    testing_indices = indices[training_set_size:]
    return training_indices, testing_indices


def run(patients, models, num_iter=1, trainset_ratio=0.8, verbose=False):

    logging.info(f"Starting model training/evaluation with: {len(patients)} patients, {num_iter} iterations,"
                 f"train_ratio={trainset_ratio}")

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
                msg = f"Training Iteration: {i}, model: {model.config.algo_name}"
                logging.info(msg)
                if verbose:
                    print(msg)

                # log ground truth for error analysis
                training_results.log_truths(i, patients, training_indices)

                training_actions, training_regrets, training_mistakes, training_payoffs, \
                training_conf_intervals, training_risks = \
                    model.run(patients, training_indices, training_results, i, is_training=True)
                # log training regret, estimated payoff & its confidence interval
                training_results.log_results(m, i, training_actions, training_regrets, training_mistakes,
                                             training_payoffs, training_conf_intervals, training_risks)

                msg = f"total regret: {training_results.get_per_iter_total_regret_for_model(m, i)}, " \
                    f"err rate: {training_results.get_per_iter_err_rate_for_model(m, i)}"
                logging.info(msg)
                if verbose:
                    print(msg)

            # testing on the test set with the model params frozen
            if trainset_ratio < 1:
                msg = f"Testing Iteration: {i}, model: {model.config.algo_name}"
                logging.info(msg)
                if verbose:
                    print(msg)

                # log ground truth for error analysis
                testing_results.log_truths(i, patients, testing_indices)

                testing_actions, testing_regrest, testing_mistakes, testing_payoffs, \
                testing_conf_intervals, testing_risks = \
                    model.run(patients, testing_indices, testing_results, i, is_training=False)
                # log testing regret, estimated payoff & its confidence interval
                testing_results.log_results(m, i, testing_actions, testing_regrest, testing_mistakes,
                                            testing_payoffs, testing_conf_intervals, testing_risks)

                msg = f"total regret: {testing_results.get_per_iter_total_regret_for_model(m, i)}, " \
                    f"err rate: {testing_results.get_per_iter_err_rate_for_model(m, i)}"
                logging.info(msg)
                if verbose:
                    print(msg)

    if trainset_ratio > 0:
        training_results.export_results()

    if trainset_ratio < 1:
        testing_results.export_results()

    # compose run summary message
    msg = f"\n------------------------\n[SUMMARY OF THE RUN: {len(models)} model(s), {len(patients)} patients, " \
        f"{num_iter} iteration(s)]\n"
    train_percentage = trainset_ratio * 100
    if trainset_ratio > 0:
        msg += f"------------------------\nTraining: {len(training_indices)} ({train_percentage}%) patients\n"
        for m in range(len(models)):
            msg += f"[{models[m].config.algo_name}] " \
                f"total regret: {training_results.get_avg_total_regret_for_model(m)}, " \
                f"err rate: {training_results.get_overall_err_rate_for_model(m)}\n"

    if trainset_ratio < 1:
        msg += f"------------------------\nTesting: {len(testing_indices)} ({100 - train_percentage}%) patients\n"
        for m in range(len(models)):
            msg += f"[{models[m].config.algo_name}] " \
                f"total regret: {testing_results.get_avg_total_regret_for_model(m)}, " \
                f"err rate: {testing_results.get_overall_err_rate_for_model(m)}\n"

    logging.info(msg)
    if verbose:
        print(msg)
