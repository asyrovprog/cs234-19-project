from v1.tools import *
import math

# For Baselines/Clinical:
#           4.0376
#           - 0.2546 x Age in decades
#           + 0.0118 x Height in cm
#           + 0.0134 x Weight in kg
#           - 0.6752 x Asian race
#           + 0.4060 x Black or African American
#           + 0.0443 x Missing or Mixed race
#           + 1.2799 x Enzyme inducer status
#           - 0.5695 x Amiodarone status

if __name__ == "__main__":
    rows = load_dataset_clinical()

    total_reward = 0
    optimal = 0
    undefined_targets = 0

    total_predictions = 0
    correct_predictions = 0

    for row in rows:
        prediction = 4.0376 \
                     - 0.2546 * row["age"] \
                     + 0.0118 * row["height"] \
                     + 0.0134 * row["weight"]  \
                     - 0.6752 * row["race_asian"] \
                     + 0.4060 * row["race_black"] \
                     + 0.0443 * row["race_missing"] \
                     + 1.2799 * row["enzyme"] \
                     - 0.5695 * row["amiodarone"]

        prediction = mg_to_dose(math.pow(prediction, 2))
        target = row["label"]

        total_reward += INCORRECT_DOSE_REWARD if prediction != target else CORRECT_DOSE_REWARD
        optimal += CORRECT_DOSE_REWARD
        total_predictions += 1
        correct_predictions += 0 if prediction != target else 1

    total_regret = optimal - total_reward

    print("Accuracy:     ", float(correct_predictions) / total_predictions)
    print("Total regret: ", total_regret)
