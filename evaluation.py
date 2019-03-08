# Utility function for evaluation.
import numpy as np
from util import *


def get_reward(action, label):
    return CORRECT_DOSE_REWARD if action == label else INCORRECT_DOSE_REWARD


def plot(model, all_regrets, all_payoffs, all_conf_intervals):

    if all_regrets is not None:
        export_plot(np.mean(all_regrets, axis=0), "Regrets", model.config.algo_name, model.config.regret_plot_output)

    if all_payoffs is not None:
        export_plot(np.mean(all_payoffs, axis=0), "Estimated Payoff", model.config.algo_name, model.config.payoff_plot_output)

    if all_conf_intervals is not None:
        export_plot(np.mean(all_conf_intervals, axis=0), "Confidence Interval", model.config.algo_name, model.config.cfinterval_plot_output)


def evaluate(patients, model, num_iter=1, verbose=False):
    indices = np.arange(len(labels))
    per_iter_regret = []
    per_iter_incorrect_frac = []

    # log all data for plotting
    all_regrets = np.full((num_iter, len(patients)), np.inf) if model.config.regret_plot_output is not None else None
    all_payoffs = np.full((num_iter, len(patients)), -np.inf) if model.config.payoff_plot_output is not None else None
    all_conf_intervals = np.zeros((num_iter, len(patients))) if model.config.cfinterval_plot_output is not None else None

    for iter in range(num_iter):
        model.reset()

        np.random.shuffle(indices)
        regrets = []
        incorrects = []
        for index in indices:
            patient = patients[index]
            features = model.get_features(patient)
            label = patient.properties[DOSE]

            action, payoff, conf_interval = model.recommend(patient)
            reward = get_reward(action, label)
            model.update(action, features, reward)

            regret = get_reward(label, label) - reward
            regrets.append(regret)
            incorrects.append(0 if action == label else 1)

            # log regret, estimated payoff & its confidence interval
            if all_regrets is not None:
                all_regrets[iter][index] = regret
            if all_payoffs is not None:
                all_payoffs[iter][index] = payoff
            if all_conf_intervals is not None:
                all_conf_intervals[iter][index] = conf_interval

        if verbose:
            print("Iteration", iter, "regret:", np.mean(regrets))

        per_iter_regret.append(np.mean(regrets))
        per_iter_incorrect_frac.append(np.mean(incorrects))

    plot(model, all_regrets, all_payoffs, all_conf_intervals)

    return np.mean(per_iter_regret), np.mean(per_iter_incorrect_frac)
