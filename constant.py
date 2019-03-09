"""
Constants for column names
"""
# Ground truth dosage
DOSE = "Therapeutic Dose of Warfarin"

# Demographics: 10
GENDER = "Gender"
AGE = "Age"
HEIGHT = "Height (cm)"
WEIGHT = "Weight (kg)"
RACE = "Race"
INDICATION = "Indication for Warfarin Treatment"
DIABETES = "Diabetes"
CHF = "Congestive Heart Failure and/or Cardiomyopathy"
VALVE_REPLACE = "Valve Replacement"
SMOKER = "Current Smoker"

# Medications: 23
MEDICATIONS = "Medications"     # list of meds
ASPIRIN = "Aspirin"
TYLENOL = "Acetaminophen or Paracetamol (Tylenol)"
WAS_DOSE = "Was Dose of Acetaminophen or Paracetamol (Tylenol) >1300mg/day"
ZOCOR = "Simvastatin (Zocor)"
LIPITOR = "Atorvastatin (Lipitor)"
LESCOL = "Fluvastatin (Lescol)"
MEVACOR = "Lovastatin (Mevacor)"
PRAVACHOL = "Pravastatin (Pravachol)"
CRESTOR = "Rosuvastatin (Crestor)"
BAYCOL = "Cerivastatin (Baycol)"
CORDARONE = "Amiodarone (Cordarone)"
TEGRETOL = "Carbamazepine (Tegretol)"
DILANTIN = "Phenytoin (Dilantin)"
RIFAMPIN = "Rifampin or Rifampicin"
SULFONAMIDE = "Sulfonamide Antibiotics"
MACROLIDE = "Macrolide Antibiotics"
ANTI_FUNGAL = "Anti-fungal Azoles"
HERBAL = "Herbal Medications, Vitamins, Supplements"
TARGET_INR = "Target INR"
EST_TARGET_INR = "Estimated Target INR Range Based on Indication"
IS_STABLE = "Subject Reached Stable Dose of Warfarin"
INR = "INR on Reported Therapeutic Dose of Warfarin"

# Genotypes: 8
CYP2C9 = "CYP2C9 consensus"
VKORC1_1639 = "VKORC1 -1639 consensus"
VKORC1_497 = "VKORC1 497 consensus"
VKORC1_1173 = "VKORC1 1173 consensus"
VKORC1_1542 = "VKORC1 1542 consensus"
VKORC1_3730 = "VKORC1 3730 consensus"
VKORC1_2255 = "VKORC1 2255 consensus"
VKORC1_4451 = "VKORC1 -4451 consensus"


VAL_UNKNOWN = -1
DOSE_LOW = 0
DOSE_MED = 1
DOSE_HIGH = 2

INCORRECT_DOSE_REWARD = -1
CORRECT_DOSE_REWARD = 0

# 2 features with numeric values
NUMERICAL_FEATURES = [HEIGHT, WEIGHT]

# 23 features with binary values
BINARY_FEATURES = [DIABETES, CHF, VALVE_REPLACE, ASPIRIN, TYLENOL, WAS_DOSE, ZOCOR, LIPITOR,
LESCOL, MEVACOR, PRAVACHOL, CRESTOR, BAYCOL, CORDARONE, TEGRETOL, DILANTIN, RIFAMPIN, SULFONAMIDE,
MACROLIDE, ANTI_FUNGAL, HERBAL, IS_STABLE, SMOKER]

