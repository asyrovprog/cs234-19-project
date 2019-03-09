import csv
import argparse
import evaluation
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
    model = get_recommender(args.algo)

    regret, incorrect_frac = evaluation.evaluate(patients, model, 50)
    accuracy = 1 - incorrect_frac
    print(f"[{model.config.algo_name}] regret={regret}; incorrect fraction={incorrect_frac}, accuracy={accuracy}")

