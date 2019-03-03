# Utility function for evaluation.
import numpy as np
import tools


def get_reward(action, label):
    return 0 if action == label else -1


def evaluate(features, labels, bandit, num_iter=1):
    indices = np.arange(len(labels))
    per_iter_regret = []
    per_iter_incorrect_frac = []
    for i in range(num_iter):
        np.random.shuffle(indices)
        regrets = []
        incorrects = []
        for i in indices:
            feature = features[i]
            label = labels[i]

            arm = bandit.recommend(feature)
            reward = get_reward(arm, label)
            bandit.update(arm, feature, reward)

            regrets.append(get_reward(label, label) - reward)
            incorrects.append(0 if arm == label else 1)

        per_iter_regret.append(np.mean(regrets))
        per_iter_incorrect_frac.append(np.mean(incorrects))

    return np.mean(per_iter_regret), np.mean(per_iter_incorrect_frac)