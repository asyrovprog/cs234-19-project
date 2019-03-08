import csv
import argparse
import evaluation
import util
from config import *
from fixed_dose import *
from clinical_dose import *
from lin_ucb import *
from patient import *


parser = argparse.ArgumentParser()
parser.add_argument("--algo", required=True, type=str,
                    choices=["fixed_dose", "clinical_dose", "linucb_disjoint"])


def get_recommender(algo):

    # default recommender: FixedDose
    model = FixedDoseRecommender(ConfigFixedDose())

    if algo == "clinical_dose":
        model = ClinicalDoseRecommender(ConfigClinicalDose())
    elif algo == "linucb_disjoint":
        model = LinUCBDisjointRecommender(ConfigLinUCBDisjoint())

    return model


def parse_all_records(records):
    """
    Parse data rows loaded from csv into list of Patient

    :param records: DictReader of the csv
    :return: list of Patient
    """
    return [Patient(r) for r in records] if records is not None else None


def load_data():
    raw_data = csv.DictReader(open("data/warfarin_5528.csv"))
    return parse_all_records(raw_data)


if __name__ == '__main__':
    args = parser.parse_args()

    patients = load_data()
    model = get_recommender(args.algo)

    regret, incorrect_frac = evaluation.evaluate(patients, model, 10)
    print(f"[{model.config.algo_name}] regret={regret}; incorrect fraction={incorrect_frac}")
