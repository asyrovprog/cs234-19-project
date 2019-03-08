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
VKORC1_4451 = "VKORC1 -4451 consensus "


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


# All numerical features.
# NUMERICAL_FEATURES = [
#     "Height (cm)",
#     "Weight (kg)"
# ]

# All binary features.
# BINARY_FEATURES = [
#     'Diabetes', 'Congestive Heart Failure and/or Cardiomyopathy', 'Valve Replacement', 'Aspirin',
#     'Acetaminophen or Paracetamol (Tylenol)', 'Was Dose of Acetaminophen or Paracetamol (Tylenol) >1300mg/day',
#     'Simvastatin (Zocor)', 'Atorvastatin (Lipitor)', 'Fluvastatin (Lescol)', 'Lovastatin (Mevacor)',
#     'Pravastatin (Pravachol)', 'Rosuvastatin (Crestor)', 'Cerivastatin (Baycol)', 'Amiodarone (Cordarone)',
#     'Carbamazepine (Tegretol)', 'Phenytoin (Dilantin)', 'Rifampin or Rifampicin', 'Sulfonamide Antibiotics',
#     'Macrolide Antibiotics', 'Anti-fungal Azoles', "Herbal Medications, Vitamins, Supplements",
#     'Subject Reached Stable Dose of Warfarin', 'Current Smoker'
# ]

# All categorical features.
"""
CATEGORICAL_FEATURES = [
    "Gender",
    "Race",
    "Ethnicity",
    "Age",
    "Indication for Warfarin Treatment","Comorbidities",
    "Diabetes",
    "Congestive Heart Failure and/or Cardiomyopathy",
    "Valve Replacement",
    "Medications",
    "Aspirin",
    "Acetaminophen or Paracetamol (Tylenol)",
    "Was Dose of Acetaminophen or Paracetamol (Tylenol) >1300mg/day",
    "Simvastatin (Zocor)",
    "Atorvastatin (Lipitor)",
    "Fluvastatin (Lescol)",
    "Lovastatin (Mevacor)",
    "Pravastatin (Pravachol)",
    "Rosuvastatin (Crestor)",
    "Cerivastatin (Baycol)",
    "Amiodarone (Cordarone)",
    "Carbamazepine (Tegretol)",
    "Phenytoin (Dilantin)",
    "Rifampin or Rifampicin",
    "Sulfonamide Antibiotics",
    "Macrolide Antibiotics",
    "Anti-fungal Azoles",
    "Herbal Medications, Vitamins, Supplements",
    "Target INR",
    "Estimated Target INR Range Based on Indication",
    "Subject Reached Stable Dose of Warfarin",
    "Current Smoker",
    "Cyp2C9 genotypes",
    "Genotyped QC Cyp2C9*2",
    "Genotyped QC Cyp2C9*3",
    "Combined QC CYP2C9",
    "VKORC1 genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T",
    "VKORC1 QC genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T",
    "VKORC1 genotype: 497T>G (5808); chr16:31013055; rs2884737; A/C",
    "VKORC1 QC genotype: 497T>G (5808); chr16:31013055; rs2884737; A/C",
    "VKORC1 genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G",
    "VKORC1 QC genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G",
    "VKORC1 genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G",
    "VKORC1 QC genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G",
    "VKORC1 genotype: 3730 G>A (9041); chr16:31009822; rs7294;  A/G",
    "VKORC1 QC genotype: 3730 G>A (9041); chr16:31009822; rs7294;  A/G",
    "VKORC1 genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G",
    "VKORC1 QC genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G",
    "VKORC1 genotype: -4451 C>A (861); Chr16:31018002; rs17880887; A/C",
    "VKORC1 QC genotype: -4451 C>A (861); Chr16:31018002; rs17880887; A/C",
    "CYP2C9 consensus",
    "VKORC1 -1639 consensus",
    "VKORC1 497 consensus",
    "VKORC1 1173 consensus",
    "VKORC1 1542 consensus",
    "VKORC1 3730 consensus",
    "VKORC1 2255 consensus",
    "VKORC1 -4451 consensus",
]
"""
