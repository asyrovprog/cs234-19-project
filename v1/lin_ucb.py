import numpy as np
from tools import *
import random

def init_vars(num_features, num_arms):
    A = np.array([np.eye(num_features).tolist()] * num_arms)
    b = np.zeros((num_arms, num_features, 1))
    theta = np.zeros((num_arms, num_features, 1))
    p = np.zeros(num_arms)
    return A, b, theta, p

def lin_ucb(dataset, num_arms, correct_reward, incorrect_reward):
    feature_size, correct, i = dataset.shape[1] - 1, 0, 0
    A, b, theta, p = init_vars(feature_size, num_arms)

    for row in dataset:
        arm = int(row[0])
        x_t = np.expand_dims(row[1:], axis=1)

        # alpha = 0
        # alpha = 0.05 / np.sqrt(i + 1)
        alpha = 0.1 / (i + 1)

        for a in range(0, num_arms):
            A_inv = np.linalg.inv(A[a])
            theta[a] = np.matmul(A_inv, b[a])
            p[a] = np.matmul(theta[a].T, x_t) + alpha * np.sqrt(np.matmul(np.matmul(x_t.T, A_inv), x_t))

        correct += 1 if np.argmax(p) == arm else 0
        i += 1

        for a in range(num_arms):
            reward = correct_reward if a == arm else incorrect_reward
            A[a] = A[a] + np.matmul(x_t, x_t.T)
            b[a] = b[a] + reward * x_t

    accuracy = float(correct) / len(dataset)
    print("Accuracy: ", float(correct) / len(dataset))
    return accuracy


if __name__ == "__main__":
    data = load_dataset_clinical()
    darr = []
    for row in data:
        r = [row["label"], row["age"],row["height"], row["weight"], row["weight"], row["race_asian"], row["race_black"], row["race_missing"], row["enzyme"], row["amiodarone"], row["male"], row["aspirin"], row["smoker"] ]
        darr.append(r)
    darr = np.array(darr)

    iters, res = 20, 0
    for i in range(iters):
        arr = np.array(darr)
        random.shuffle(arr)
        res += lin_ucb(arr, 3, CORRECT_DOSE_REWARD, INCORRECT_DOSE_REWARD)
    print("Average accuracy: ", res / iters)
