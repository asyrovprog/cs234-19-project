import csv
import argparse
import evaluation
import util
from config import *
from fixed_dose import *
from clinical_dose import *
from lin_ucb import *


parser = argparse.ArgumentParser()
parser.add_argument("--algo", required=True, type=str,
                    choices=["fixed_dose", "clinical_dose", "linucb_disjoint"])


def get_recommender(algo, features):

    # default recommender: FixedDose
    model = FixedDoseRecommender(ConfigFixedDose())

    if algo == "clinical_dose":
        model = ClinicalDoseRecommender(ConfigClinicalDose())
    elif algo == "linucb_disjoint":
        model = LinUCBDisjointRecommender(ConfigLinUCBDisjoint(), features.shape[1])

    return model


def load_data():
    raw_data = csv.DictReader(open("data/warfarin_5528_imputed.csv"))
    return util.process_data(raw_data, keep_missing_data=False)


if __name__ == '__main__':
    args = parser.parse_args()

    features, labels = load_data()
    model = get_recommender(args.algo, features)

    regret, incorrect_frac = evaluation.evaluate(features, labels, model, 10)
    print(f"[{model.config.algo_name}] regret={regret}; incorrect fraction={incorrect_frac}")

    # total_regret, correct_predictions, total_predictions = model.run(raw_data)
    #
    # print(f"results: accuracy={correct_predictions/total_predictions}, regret={total_regret}")
