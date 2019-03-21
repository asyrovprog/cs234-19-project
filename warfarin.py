import csv
import os
import argparse
import evaluation
import logging
from config import *
from fixed_dose import *
from clinical_dose import *
from lin_ucb import *
from tree_heuristic import *
from patient import *
from lasso_bandit import *
from ensemble_majority3 import *


parser = argparse.ArgumentParser()
parser.add_argument("--algo", required=True, type=str,
                    choices=ALGOS + ["all"])
parser.add_argument("--iter", required=False, type=int)
parser.add_argument("--train_ratio", required=False, type=float)


def get_recommender(algo, output_path):

    # default recommender: FixedDose
    model = FixedDoseRecommender(get_config(algo, output_path))

    if algo == "clinical_dose":
        model = ClinicalDoseRecommender(get_config(algo, output_path))
    elif algo == "linucb_disjoint":
        model = LinUCBDisjointRecommender(get_config(algo, output_path))
    elif algo == "linucb_disjoint_basic":
        model = LinUCBDisjointBasicRecommender(get_config(algo, output_path))
    elif algo.startswith("tree"):
        model = TreeHeuristicRecommender(get_config(algo, output_path))
    elif algo == "lasso":
        model = LassoBandit(get_config(algo, output_path))
    elif algo == "majority3":
        model = Majority3Recommender(get_config(algo, output_path))
    return model


def parse_all_records(records, keep_missing=False):
    """
    Parse data rows loaded from csv into list of Patient

    :param records: DictReader of the csv
    :return: list of Patient
    """
    results = list()
    rawCount = 0
    for r in records:
        rawCount += 1
        patient = Patient(r)
        # filter out records with missing essential data
        if keep_missing or not (patient.properties[AGE] is AgeGroup.unknown or
                                patient.properties[HEIGHT] == VAL_UNKNOWN or
                                patient.properties[WEIGHT] == VAL_UNKNOWN or
                                patient.properties[DOSE] == VAL_UNKNOWN):
            results.append(patient)
    logging.info(f"Parsing raw records: loaded record count={rawCount}, returned patient count={len(results)}, "
                 f"keep_missing={keep_missing}")
    return results


def load_data(filename):
    logging.info(f"Loading data set from: {filename}")
    raw_data = csv.DictReader(open(filename))
    return parse_all_records(raw_data, keep_missing=False)


if __name__ == '__main__':
    args = parser.parse_args()

    output_path = "results/{}/".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    # directory for outputs
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    log_path = output_path + "log.txt"
    logging.basicConfig(filename=log_path, format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
    datafile = "data/warfarin.csv"
    patients = load_data(datafile)
    models = []
    logging.info(f"Initializing recommender model(s): {args.algo}")

    if args.algo == "all":  # run all models
        models += [get_recommender(algo, output_path) for algo in ALGOS]
    else:   # run a single model
        models += [get_recommender(args.algo, output_path)]

    iters = args.iter if args.iter else 1
    train_ratio = args.train_ratio if args.train_ratio is not None else 0.8

    evaluation.run(patients, models, iters, train_ratio, verbose=True)
