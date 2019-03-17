import sys
import csv
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from constant import *


def undefined(s):
    if isinstance(s, str):
        s = s.strip()
    return s is None or s == "NA" or s == ""


def clean_value(s):
    result = s
    if undefined(s):
        result = None
    elif isinstance(s, str):
        result = s.strip().lower()
    return result


def get_float(s):
    value = clean_value(s)

    if value is not None:
        try:
            value = float(s)
        except ValueError:
            value = VAL_UNKNOWN
    else:
        value = VAL_UNKNOWN

    return value


def get_int(s):
    value = clean_value(s)
    if value is not None:
        try:
            value = int(s)
        except ValueError:
            value = VAL_UNKNOWN
    else:
        value = VAL_UNKNOWN

    return value


def export_stats_list(stats_list, filename):
    """
    Export a stats list to a file

    Args:
        stats_list: (list) of stats in float / int
        filename: (string) directory
    """
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(stats_list)


def export_plot(ys, ylabel, title, filename):
    """
    Export a plot in filename

    Args:
        ys: (list) of float / int to plot
        filename: (string) directory
    """
    plt.figure()
    plt.plot(range(len(ys)), ys)
    plt.xlabel("Patient Count")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename)
    plt.close()


#
# https://math.stackexchange.com/questions/102978/incremental-computation-of-standard-deviation
#
def variance_update(prev_s2, n, prev_mu, x_n):
    s2 = ((n - 2)/(n - 1))*prev_s2  if n > 2 else 0
    s2 += (1/n) * pow((x_n - prev_mu), 2)
    return s2


def mean_update(prev_mu, n, x_n):
    return (1/n)*(x_n + (n - 1)*prev_mu)


def print_flush(s, end='\n'):
    print(s, end=end)
    sys.stdout.flush()
