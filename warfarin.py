import csv
import argparse
import evaluation
from config import *
from fixed_dose import *
from clinical_dose import *
from lin_ucb import *
from tree_heuristic import *
from patient import *
from lasso_bandit import *


parser = argparse.ArgumentParser()
parser.add_argument("--algo", required=True, type=str,
                    choices=ALGOS + ["all"])
parser.add_argument("--iter", required=False, type=int)
parser.add_argument("--train_ratio", required=False, type=float)


def get_recommender(algo):

    # default recommender: FixedDose
    model = FixedDoseRecommender(ConfigFixedDose())

    if algo == "clinical_dose":
        model = ClinicalDoseRecommender(ConfigClinicalDose())
    elif algo == "linucb_disjoint":
        model = LinUCBDisjointRecommender(ConfigLinUCBDisjoint())
    elif algo == "tree_heuristics":
        model = TreeHeuristicRecommender(ConfigTreeHeuristic())
    elif algo == "lasso":
        model = LassoBandit(ConfigLasso())
    return model


def parse_all_records(records, keep_missing=True):
    """
    Parse data rows loaded from csv into list of Patient

    :param records: DictReader of the csv
    :return: list of Patient
    """
    results = list()
    for r in records:
        patient = Patient(r)
        if keep_missing or (patient.properties[AGE] is AgeGroup.unknown or patient.properties[HEIGHT] == VAL_UNKNOWN \
            or patient.properties[WEIGHT] == VAL_UNKNOWN or patient.properties[DOSE] == VAL_UNKNOWN):
            results.append(patient)

    return results


def load_data():
    raw_data = csv.DictReader(open("data/warfarin.csv"))
    return parse_all_records(raw_data)


if __name__ == '__main__':
    args = parser.parse_args()

    patients = load_data()
    models = []
    if args.algo == "all":  # run all models
        models += [get_recommender(algo) for algo in ALGOS]
    else:   # run a single model
        models += [get_recommender(args.algo)]

    iters = args.iter if args.iter else 1
    train_ratio = args.train_ratio if args.train_ratio is not None else 0.8

    evaluation.run(patients, models, iters, train_ratio, verbose=True)
