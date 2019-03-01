import csv

TARGET = "Therapeutic Dose of Warfarin"

DOSE_NA = -1
DOSE_LOW = 0
DOSE_MED = 1
DOSE_HIGH = 2

INCORRECT_DOSE_REWARD = -1
CORRECT_DOSE_REWARD = 0

def load_dataset():
    input_file = csv.DictReader(open("data/warfarin.csv"))
    return input_file

#
# convert dose (string) to na/low/med/high integers
#
def mg_to_dose(d):
    if d == "NA" or d == "":
        return DOSE_NA
    d = float(d)
    if d <= 21:
        return DOSE_LOW
    return DOSE_MED if d <= 49 else DOSE_HIGH

#
# For Baselines/Fixed Dose we just need one field "Therapeutic Dose of Warfarin"
# converted to:
#      0 -  0..21 mg/week  (LOW)
#      1 - 21..49 mg/week  (MEDIUM)
#      2 - 21..49 mg/week  (HIGH)
#
def load_dataset_fixed_dose():
    rows = load_dataset()
    ds = [mg_to_dose(row[TARGET]) for row in rows]
    return ds
