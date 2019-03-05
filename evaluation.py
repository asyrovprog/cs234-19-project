# Utility function for evaluation.
import numpy as np
from constant import *


def get_reward(action, label):
    return CORRECT_DOSE_REWARD if action == label else INCORRECT_DOSE_REWARD


def evaluate(features, labels, model, num_iter=1, verbose=False):
    indices = np.arange(len(labels))
    per_iter_regret = []
    per_iter_incorrect_frac = []
    for iter in range(num_iter):
        model.reset()

        np.random.shuffle(indices)
        regrets = []
        incorrects = []
        for index in indices:
            feature = features[index]
            label = labels[index]

            # TODO: log estimated payoff & its confidence interval
            # TODO: plot estimated payoff & its confidence interval
            arm, payoff, conf_interval = model.recommend(feature)
            reward = get_reward(arm, label)
            model.update(arm, feature, reward)

            regrets.append(get_reward(label, label) - reward)
            incorrects.append(0 if arm == label else 1)

        if verbose:
            print("Iteration", iter, "regret:", np.mean(regrets))

        per_iter_regret.append(np.mean(regrets))
        per_iter_incorrect_frac.append(np.mean(incorrects))

    return np.mean(per_iter_regret), np.mean(per_iter_incorrect_frac)
