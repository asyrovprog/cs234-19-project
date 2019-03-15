import numpy as np
import matplotlib.pyplot as plt

def fill_plot(mean, var, filename, label):
    x = range(len(mean))
    mean = np.array(mean)
    std = np.sqrt(np.array(var))
    plt.plot(mean, label=label)
    plt.legend(loc='lower right')
    plt.fill_between(x, mean-std, mean+std, alpha=0.3)
    plt.grid(True)
    plt.savefig(fname=filename)
