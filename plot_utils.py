import numpy as np
import matplotlib.pyplot as plt

def fill_plot(mean, filename, label):
    N = 100
    x = [i for i in range(len(mean))]
    mean = np.array(mean)

    avg_mask = np.ones(N) / N
    mean = np.convolve(mean, avg_mask, 'full')[:-N+1]

    plt.plot(x, mean, label=label)
    plt.legend(loc='lower right')

    plt.ylim(top=0.85)
    plt.ylim(bottom=0)  # adjust the bottom leaving top unchanged
    plt.grid(True)
    plt.savefig(fname=filename)
