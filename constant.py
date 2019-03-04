# Constants
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

# All numerical features.
NUMERICAL_FEATURES = [
    "Height (cm)",
    "Weight (kg)"
]

# All categorical features.
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

