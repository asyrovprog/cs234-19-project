from feature import *
from preprocess import *
from util import *


class Patient:
    """
    Class to represent a patient
    ------------------------------------------------
    Gender *
    Race *
    Age *
    Height (cm) *
    Weight (kg) *
    Indication for Warfarin Treatment *
    Diabetes *
    Congestive Heart Failure and/or Cardiomyopathy *
    Valve Replacement *
    Medications *
    Aspirin *
    Acetaminophen or Paracetamol (Tylenol) *
    Was Dose of Acetaminophen or Paracetamol (Tylenol) >1300mg/day *
    Simvastatin (Zocor) *
    Atorvastatin (Lipitor) *
    Fluvastatin (Lescol) *
    Lovastatin (Mevacor) *
    Pravastatin (Pravachol) *
    Rosuvastatin (Crestor) *
    Cerivastatin (Baycol) *
    Amiodarone (Cordarone) *
    Carbamazepine (Tegretol) *
    Phenytoin (Dilantin) *
    Rifampin or Rifampicin *
    Sulfonamide Antibiotics *
    Macrolide Antibiotics *
    Anti-fungal Azoles *
    "Herbal Medications, Vitamins, Supplements" *
    Target INR *
    Estimated Target INR Range Based on Indication (maybe?)
    Subject Reached Stable Dose of Warfarin *
    Therapeutic Dose of Warfarin (label)
    INR on Reported Therapeutic Dose of Warfarin (maybe?)
    Current Smoker *
    CYP2C9 consensus *
    VKORC1 -1639 consensus *
    VKORC1 497 consensus *
    VKORC1 1173 consensus *
    VKORC1 1542 consensus *
    VKORC1 3730 consensus *
    VKORC1 2255 consensus *
    VKORC1 -4451 consensus *
    ------------------------------------------------
    """
    def __init__(self, record):
        self.properties = dict()
        self.properties[DOSE] = parse_dose(record[DOSE])
        self.properties[GENDER] = parse_gender(record[GENDER])
        self.properties[RACE] = parse_race(record[RACE])
        self.properties[AGE] = parse_age_group(record[AGE])
        for p in NUMERICAL_FEATURES:
            self.properties[p] = get_float(record[p])
        self.properties[INDICATION] = parse_indications(record[INDICATION])
        for p in BINARY_FEATURES:
            self.properties[p] = parse_binary_feature(record[p])
        self.properties[MEDICATIONS] = parse_medications(record[MEDICATIONS])
        self.properties[CYP2C9] = parse_genotype_CYP2C9(record[CYP2C9])
        self.properties[VKORC1_497] = parse_genotype_VKORC1_497(record[VKORC1_497])
        self.properties[VKORC1_1173] = parse_genotype_VKORC1_1173(record[VKORC1_1173])
        self.properties[VKORC1_1542] = parse_genotype_VKORC1_1542(record[VKORC1_1542])
        self.properties[VKORC1_3730] = parse_genotype_VKORC1_3730(record[VKORC1_3730])
        self.properties[VKORC1_2255] = parse_genotype_VKORC1_2255(record[VKORC1_2255])
        self.properties[VKORC1_4451] = parse_genotype_VKORC1_4451(record[VKORC1_4451])
        self.properties[VKORC1_1639] = parse_genotype_VKORC1_1639(record[VKORC1_1639],
                                                                  self.properties[RACE],
                                                                  self.properties[VKORC1_2255],
                                                                  self.properties[VKORC1_1173],
                                                                  self.properties[VKORC1_1542])


