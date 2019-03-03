# Utility function for evaluation.
import numpy as np


def get_reward(action, label):
    return 0 if action == label else -1


def evaluate(features, labels, bandit, num_iter=1):
    indices = np.arange(len(labels))
    per_iter_reward = []
    for i in range(num_iter):
        np.random.shuffle(indices)
        rewards = []
        for i in indices:
            feature = features[i]
            label = labels[i]

            arm = bandit.recommend(feature)
            reward = get_reward(arm, label)
            rewards.append(reward)
            bandit.update(arm, feature, reward)
        per_iter_reward.append(np.mean(rewards))
    return np.mean(per_iter_reward)