from tools import *


if __name__ == "__main__":
    rows = load_dataset_fixed_dose()

    total_reward = 0
    optimal = 0
    undefined_targets = 0

    total_predictions = 0
    correct_predictions = 0

    for dose in rows:
        if dose == DOSE_NA:
            # we do not have label for this parient, so skip this record
            undefined_targets += 1
        else:
            total_reward += INCORRECT_DOSE_REWARD if dose != DOSE_MED else CORRECT_DOSE_REWARD
            optimal += CORRECT_DOSE_REWARD
            total_predictions += 1
            correct_predictions += 0 if dose != DOSE_MED else 1

    total_regret = optimal - total_reward

    print("Accuracy:     ", float(correct_predictions) / total_predictions)
    print("Total regret: ", total_regret)
    print("Rowcount:     ", len(rows) - undefined_targets)



