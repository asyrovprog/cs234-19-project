import csv
import pandas as pd
from constant import *
import sklearn.preprocessing
import sklearn.impute
import numpy as np

def load_dataset():
    input_file = csv.DictReader(open("data/warfarin.csv"))
    return input_file

def undefined(s):
    return s == "NA" or s == ""

#
# convert dose (string) to na/low/med/high integers
#      0 - <21 mg/week  (LOW)
#      1 - <=49 mg/week  (MEDIUM)
#      2 - else mg/week  (HIGH)
#
def mg_to_dose(d):
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

#
# For Baselines/Fixed Dose we just need one field "Therapeutic Dose of Warfarin"
#
def load_dataset_fixed_dose():
    rows = load_dataset()
    ds = [mg_to_dose(row[TARGET]) for row in rows]
    missing_data = sum([1 if v == DOSE_NA else 0 for v in ds])
    if missing_data > 0:
        print("WARNING: ", missing_data, " records have missing data. They will not be processed.")
    return ds

#
# For Baselines Clinical
#
def load_dataset_clinical(keep_missing_data=False):
    rows = load_dataset()
    result = []
    missing_count = 0
    for row in rows:
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
                or row["Carbamazepine (Tegretol)"] == "1"\
                or row["Phenytoin (Dilantin)"] == "1" else 0

            amiodarone = 1 if "amiodarone" in meds \
                or row["Amiodarone (Cordarone)"] == "1" else 0

            male = 1 if row["Gender"] == "male" else 0
            aspirin = 1 if "aspirin" in meds else 0
            smoker = 1 if row["Current Smoker"] == "1" else 0

            result.append({"label": label, "age":  age, "height" : height, "weight": weight, "race_asian": asian,
                           "race_black": black, "race_missing": missing, "enzyme": enzyme, "amiodarone": amiodarone,
                           # additional fields not used in clinical, but used in TF
                           "male": male, "aspirin": aspirin, "smoker": smoker})
        else:
            missing_count += 1

    if missing_count > 0:
        print("WARNING:", missing_count, "records have missing data. They will not be processed." )
    return result


def load_dataset_bandit(features_to_include=None):
    """Get data set used to evaluate bandit algorithm.
    Args:
        features_to_include: a list features to include in the output. If None, include all.
    Returns:
        feature matrix, label.
    """
    data = pd.read_csv("data/warfarin_imputed_missing.csv")

    # Drop row without label.
    data = data[data[TARGET].notna()]

    # Convert to discrete label.
    def _to_dose(d):
        if d < 21:
            return DOSE_LOW
        if d < 49:
            return DOSE_MED
        return DOSE_HIGH

    labels = data[TARGET].apply(_to_dose).values

    numeric_features_to_include = set(NUMERICAL_FEATURES)
    categorical_features_to_include = set(CATEGORICAL_FEATURES)

    if features_to_include is not None:
        numeric_features_to_include = numeric_features_to_include.intersection(set(features_to_include))
        categorical_features_to_include = categorical_features_to_include.intersection(set(features_to_include))

    features = data.loc[:, data.columns != TARGET]
    numeric_features = features[numeric_features_to_include]
    # TODO: parse "medication" feature. Currently it is treated as simple
    # categorical this is definitely incorrect.
    categorical_features = features[categorical_features_to_include]
    numeric_categorical_features = categorical_features.select_dtypes("float64")
    string_categorical_features = categorical_features.select_dtypes("object")

    # Impute missing value for numeric features.
    imp_mean = sklearn.impute.SimpleImputer(missing_values=np.nan, strategy="mean")
    numeric_features = imp_mean.fit_transform(numeric_features)
    numeric_features = sklearn.preprocessing.scale(numeric_features)

    # Compute onehot encoding for categorical features.
    imp_constant = sklearn.impute.SimpleImputer(missing_values=np.nan, strategy="constant")
    numeric_categorical_features = imp_constant.fit_transform(numeric_categorical_features)
    string_categorical_features = imp_constant.fit_transform(string_categorical_features)

    onehot = sklearn.preprocessing.OneHotEncoder(sparse=False)
    numeric_categorical_features = onehot.fit_transform(numeric_categorical_features)
    string_categorical_features = onehot.fit_transform(string_categorical_features)

    return np.hstack((numeric_features, numeric_categorical_features, string_categorical_features)), labels