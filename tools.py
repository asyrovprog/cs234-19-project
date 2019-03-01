import csv

# fields
TARGET = "Therapeutic Dose of Warfarin"
AGE="Age"
HEIGHT="Height (cm)"
WEIGHT="Weight (kg)"
RACE="Race"
MEDICATIONS = "Medications"
CARBAMAZEPINE = "Carbamazepine (Tegretol)"

DOSE_NA = -1
DOSE_LOW = 0
DOSE_MED = 1
DOSE_HIGH = 2

INCORRECT_DOSE_REWARD = -1
CORRECT_DOSE_REWARD = 0

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
def load_dataset_clinical():
    rows = load_dataset()
    result = []
    missing_count = 0
    for row in rows:
        age = get_age_decades(row)
        label = mg_to_dose(row[TARGET])
        height = get_float_fld(row, HEIGHT)
        weight = get_float_fld(row, WEIGHT)

        if not -1 in [age, label, height, weight]:

            asian = get_race(row, "Asian")
            black = get_race(row, "Black or African American")
            missing = 1 if row[RACE].lower() in {"", "na", "unknown"} else 0

            meds = {m.strip(" ").lower() for m in row[MEDICATIONS].split(";")}

            enzyme = 1 if  {"carbamazepine", "phenytoin", "rifampin", "rifampicin"} & meds \
                or row["Rifampin or Rifampicin"] == "1" \
                or row["Carbamazepine (Tegretol)"] == "1"\
                or row["Phenytoin (Dilantin)"] == "1" else 0

            amiodarone = 1 if "amiodarone" in meds \
                or row["Amiodarone (Cordarone)"] == "1" else 0

            result.append({ "label": label, "age":  age, "height" : height, "weight": weight, "race_asian": asian,
                            "race_black": black, "race_missing": missing, "enzyme": enzyme, "amiodarone": amiodarone})

        else:
            missing_count += 1

    if missing_count > 0:
        print("WARNING: ", missing_count, " records have missing data. They will not be processed." )
    return result