import logging
import re
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from constant import *


def undefined(s):
    if isinstance(s, str):
        s = s.strip()
    return s == "NA" or s == ""


def clean_value(s):
    result = s
    if isinstance(s, str):
        result = s.strip().lower()
        if result == "":
            result = None
    return result


def mg_to_dose(d):

    """
    convert dose (string) to na/low/med/high integers
        0: < 21 mg/week  (LOW)
        1: <= 49 mg/week  (MEDIUM)
        2: else mg/week  (HIGH)
    """
    if undefined(d):
        return VAL_UNKNOWN
    if isinstance(d, str):
        d = d.strip()
    d = float(d)
    if d < 21:
        return DOSE_LOW
    return DOSE_MED if d <= 49 else DOSE_HIGH


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
    if undefined(s):
        return VAL_UNKNOWN
    try:
        value = float(s.strip())
    except ValueError:
        value = VAL_UNKNOWN

    return value


def get_race(s, expected):
    return 1 if s.strip().lower() == expected.lower() else 0


def process_data(raw_data, keep_missing_data=False):
    features = []
    labels = []
    missing_count = 0
    for row in raw_data:
        age = get_age_decades(row[AGE])
        label = mg_to_dose(row[DOSE])
        height = get_float(row[HEIGHT])
        weight = get_float(row[WEIGHT])
        if (not VAL_UNKNOWN in [age, label, height, weight]) or keep_missing_data:
            asian = get_race(row[RACE], "Asian")
            black = get_race(row[RACE], "Black or African American")
            missing = 1 if row[RACE].lower() in {"", "na", "unknown"} else 0

            meds = {m.strip(" ").lower() for m in row[MEDICATIONS].split(";")}

            enzyme = 1 if {"carbamazepine", "phenytoin", "rifampin", "rifampicin"} & meds \
                          or row["Rifampin or Rifampicin"] == "1" \
                          or row["Carbamazepine (Tegretol)"] == "1" \
                          or row["Phenytoin (Dilantin)"] == "1" else 0

            amiodarone = 1 if "amiodarone" in meds \
                              or row["Amiodarone (Cordarone)"] == "1" else 0

            male = 1 if row["Gender"].strip().lower() == "male" else 0
            aspirin = 1 if "aspirin" in meds else 0
            smoker = 1 if row["Current Smoker"] == "1" else 0

            features.append([age, height, weight, asian, black, missing, enzyme,
                            amiodarone, male, aspirin, smoker])

            labels.append(label)

        else:
            missing_count += 1

    if missing_count > 0:
        print("WARNING:", missing_count, "records have missing data. They will not be processed.")

    # TODO: add one-hot encoding for categorical features.

    return np.array(features), np.array(labels)


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
