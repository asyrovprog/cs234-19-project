import logging
import numpy as np
from constant import *


def undefined(s):
    return s == "NA" or s == ""


def mg_to_dose(d):

    """
    convert dose (string) to na/low/med/high integers
        0: < 21 mg/week  (LOW)
        1: <= 49 mg/week  (MEDIUM)
        2: else mg/week  (HIGH)
    """
    if undefined(d):
        return DOSE_NA
    d = float(d)
    if d < 21:
        return DOSE_LOW
    return DOSE_MED if d <= 49 else DOSE_HIGH


def get_age_decades(row):
    age_str = row[AGE]
    if undefined(age_str):
        return -1
    age_str = age_str.replace(" ", "")
    if "-" in age_str:
        age_str = age_str.split("-")[0]
    age_str = age_str.replace("+", "")
    return int(float(age_str) / 10)


def get_float_fld(row, fld):
    v = row[fld]
    if undefined(v):
        return -1
    return float(v)


def get_race(row, expected):
    v = row[RACE]
    return 1 if v.lower() == expected.lower() else 0


def process_data(raw_data, keep_missing_data=False):
    features = []
    labels = []
    missing_count = 0
    for row in raw_data:
        age = get_age_decades(row)
        label = mg_to_dose(row[TARGET])
        height = get_float_fld(row, HEIGHT)
        weight = get_float_fld(row, WEIGHT)
        if (not -1 in [age, label, height, weight]) or keep_missing_data:
            asian = get_race(row, "Asian")
            black = get_race(row, "Black or African American")
            missing = 1 if row[RACE].lower() in {"", "na", "unknown"} else 0

            meds = {m.strip(" ").lower() for m in row[MEDICATIONS].split(";")}

            enzyme = 1 if {"carbamazepine", "phenytoin", "rifampin", "rifampicin"} & meds \
                          or row["Rifampin or Rifampicin"] == "1" \
                          or row["Carbamazepine (Tegretol)"] == "1" \
                          or row["Phenytoin (Dilantin)"] == "1" else 0

            amiodarone = 1 if "amiodarone" in meds \
                              or row["Amiodarone (Cordarone)"] == "1" else 0

            male = 1 if row["Gender"] == "male" else 0
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
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    return logger
