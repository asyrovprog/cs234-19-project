import logging
import re
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


def get_age_decades(s):
    match = re.match(r'^\s*(\d+)\s*[-+].*', s.strip())
    if match:
        try:
            age = int(match.group(1))
            age = age // 10
        except ValueError:
            age = VAL_UNKNOWN
        return age
    else:
        return VAL_UNKNOWN


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


def get_logger(filename):
    """
    Return a logger instance to a file
    """
    logger = logging.getLogger('logger')
    logger.setLevel(logging.ERROR)
    logging.basicConfig(format='%(message)s', level=logging.ERROR)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    return logger


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
