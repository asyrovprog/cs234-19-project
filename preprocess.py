import re
import numpy as np
from feature import *
from util import *


def feature_scaling(min, max, value):
    """
    Perform Min-Max Scaling on the given value based on the provided min and max range

    :param min: minimum value
    :param max: maximum value
    :param value: actual value
    :return:
    """
    scaled = VAL_UNKNOWN
    if value is not None and min is not None and max is not None and max > min:
        scaled = (value - min) / (max - min)
    return scaled


def get_bmi(height, weight):
    """
    Calculate Body Mass Index (BMI) for the given height and weight
    formula: weight (kg) / height^2 (m)

    :param height: height in cm
    :param weight: weight in kg
    :return:
    """
    bmi = VAL_UNKNOWN
    if height is not None and weight is not None and height > 0 and weight > 0:
        bmi = weight * 10000 / (height ** 2)
    return bmi


def get_one_hot(enum_value):
    """
    Convert enum value into one hot vector

    :param enum_value: input categorical enum value
    :return: one hot vector for the given enum value
    """
    enum_type = type(enum_value)
    results = [0] * len(enum_type)
    enum_list = list(enum_type)
    if enum_value in enum_list:
        results[enum_list.index(enum_value)] = 1
    return results


def get_one_hot_from_list(enum_value_list):
    results = []
    if enum_value_list is not None and len(enum_value_list) > 0:
        enum_type = type(enum_value_list[0])
        results = [0] * len(enum_type)
        enum_list = list(enum_type)
        for enum_value in enum_value_list:
            if enum_value in enum_list:
                results[enum_list.index(enum_value)] = 1
    return results


def parse_dose(d):
    """
    convert dose (string) to na/low/med/high integers
        0: < 21 mg/week  (LOW)
        1: <= 49 mg/week  (MEDIUM)
        2: else mg/week  (HIGH)
    """
    result = get_float(d)

    if result != VAL_UNKNOWN:
        if result < 21:
            result = DOSE_LOW
        elif result <= 49:
            result = DOSE_MED
        else:
            result = DOSE_HIGH

    return result


def parse_gender(s):
    """
    Parse 'Gender' column in the csv and return corresponding Gender enum

    :param s: input string
    :return: Gender enum
    """
    gender = Gender.unknown
    s = clean_value(s)
    if s == "male":
        gender = Gender.male
    elif s == "female":
        gender = Gender.female
    return gender


def parse_race(s):
    """
    Parse 'Race' column in the csv and return corresponding Race enum

    :param s: input string
    :return: Race enum
    """
    race = Race.unknown
    s = clean_value(s)
    if s == "asian":
        race = Race.asian
    elif s == "white":
        race = Race.white
    elif s == "black or african american":
        race = Race.black
    return race


def parse_age_group(s):
    """
    Parse 'Age' column in the csv and return corresponding AgeGroup enum

    :param s: input string
    :return: AgeGroup enum
    """
    age_group = AgeGroup.unknown
    s = clean_value(s)
    if s is not None:
        match = re.match(r'^\s*(\d+)\s*[-+].*', s)
        if match:
            try:
                age = int(match.group(1))
                age_group = AgeGroup(age // 10)
            except ValueError:
                age_group = AgeGroup.unknown

    return age_group


def parse_indications(s):
    """
    Parse 'Indication for Warfarin Treatment' column in the csv and
    return a list of Indication enums

    :param s: input string
    :return: list of Indication enums
    """
    results = [Indication.unknown]
    s = clean_value(s)
    if s is not None:
        inds = re.findall(r"\d+", s)
        try:
            results = [Indication(int(clean_value(i))) for i in inds]
        except ValueError:
            results = [Indication.unknown]

    return results


def parse_medications(s):
    """
    Parse 'Medications' column in the csv and return a list of medication strings

    :param s: input string
    :return: list of normalized medication strings
    """
    results = []
    s = clean_value(s)
    if s is not None:
        meds = re.split(r"[;,]", s)
        results = [(clean_value(i)) for i in meds]

    return results


def parse_binary_feature(d):
    result = get_int(d)
    return None if result is None else BinaryFeature(result)


def parse_genotype_CYP2C9(s):
    """
    Parse 'CYP2C9 consensus' column in the csv and return a list of GenoCYP2C9 enums

    :param s: input string ['*2/*3', '*3/*3', '*1/*1', '*1/*3', nan, '*2/*2', '*1/*2',
       '*1/*14', '*1/*13', '*1/*11', '*1/*5', '*1/*6']
    :return: list of GenoCYP2C9 enums
    """
    results = [GenoCYP2C9.unknown]
    s = clean_value(s)
    if s is not None:
        genos = re.findall(r"\d+", s)
        try:
            results = [GenoCYP2C9(int(clean_value(i))) for i in genos]
        except ValueError:
            results = [GenoCYP2C9.unknown]

    return results


def parse_genotype_VKORC1_497(s):
    """
    Parse 'VKORC1 497 consensus' column in the csv and return a list of GenoVKORC1_497 enums

    :param s: input string [nan, 'G/T', 'T/T', 'G/G']
    :return: list of GenoVKORC1_497 enums
    """
    geno = GenoVKORC1_497.unknown
    s = clean_value(s)
    if s == "g/g":
        geno = GenoVKORC1_497.g_g
    elif s == "g/t":
        geno = GenoVKORC1_497.g_t
    elif s == "t/t":
        geno = GenoVKORC1_497.t_t
    return geno


def parse_genotype_VKORC1_1173(s):
    """
    Parse 'VKORC1 1173 consensus' column in the csv and return a list of GenoVKORC1_1173 enums

    :param s: input string [nan, 'T/T', 'C/T', 'C/C']
    :return: list of GenoVKORC1_1173 enums
    """
    geno = GenoVKORC1_1173.unknown
    s = clean_value(s)
    if s == "c/c":
        geno = GenoVKORC1_1173.c_c
    elif s == "c/t":
        geno = GenoVKORC1_1173.c_t
    elif s == "t/t":
        geno = GenoVKORC1_1173.t_t
    return geno


def parse_genotype_VKORC1_1542(s):
    """
    Parse 'VKORC1 1542 consensus' column in the csv and return a list of GenoVKORC1_1542 enums

    :param s: input string [nan, 'C/C', 'C/G', 'G/G']
    :return: list of GenoVKORC1_1542 enums
    """
    geno = GenoVKORC1_1542.unknown
    s = clean_value(s)
    if s == "c/c":
        geno = GenoVKORC1_1542.c_c
    elif s == "c/g":
        geno = GenoVKORC1_1542.c_g
    elif s == "g/g":
        geno = GenoVKORC1_1542.g_g
    return geno


def parse_genotype_VKORC1_3730(s):
    """
    Parse 'VKORC1 3730 consensus' column in the csv and return a list of GenoVKORC1_3730 enums

    :param s: input string [nan, 'G/G', 'A/G', 'A/A']
    :return: list of GenoVKORC1_3730 enums
    """
    geno = GenoVKORC1_3730.unknown
    s = clean_value(s)
    if s == "a/a":
        geno = GenoVKORC1_3730.a_a
    elif s == "a/g":
        geno = GenoVKORC1_3730.a_g
    elif s == "g/g":
        geno = GenoVKORC1_1542.g_g
    return geno


def parse_genotype_VKORC1_2255(s):
    """
    Parse 'VKORC1 2255 consensus' column in the csv and return a list of GenoVKORC1_2255 enums

    :param s: input string [nan, 'T/T', 'C/T', 'C/C']
    :return: list of GenoVKORC1_2255 enums
    """
    geno = GenoVKORC1_2255.unknown
    s = clean_value(s)
    if s == "c/c":
        geno = GenoVKORC1_2255.c_c
    elif s == "c/t":
        geno = GenoVKORC1_2255.c_t
    elif s == "t/t":
        geno = GenoVKORC1_2255.t_t
    return geno


def parse_genotype_VKORC1_4451(s):
    """
    Parse 'VKORC1 -4451 consensus' column in the csv and return a list of GenoVKORC1_4451 enums

    :param s: input string [nan, 'A/C', 'C/C', 'A/A']
    :return: list of GenoVKORC1_4451 enums
    """
    geno = GenoVKORC1_4451.unknown
    s = clean_value(s)
    if s == "a/a":
        geno = GenoVKORC1_4451.a_a
    elif s == "a/c":
        geno = GenoVKORC1_4451.a_c
    elif s == "c/c":
        geno = GenoVKORC1_4451.c_c
    return geno


def impute_genotype_VKORC1_1639(race, vkorc1_2255, vkorc1_1173, vkorc1_1542):
    """
    Impute missing VKORC1 -1639 SNP rs9923231 according to p.13 of appx.pdf, section S4.
    :param: 4 other supporting columns: race, vkorc1_2255, vkorc1_1173, vkorc1_1542
    :return: imputed GenoVKORC1_1639 enum
    """
    # If Race is not "Black or African American" or "Missing or Mixed Race"
    # and rs2359612='C/C' then impute rs9923231='G/G'
    if race is not Race.black and race is not Race.unknown and vkorc1_2255 is GenoVKORC1_2255.c_c:
        return GenoVKORC1_1639.g_g

    # If Race is not "Black or African American" or "Missing or Mixed Race"
    # and rs2359612='T/T' then impute rs9923231='A/A'
    if race is not Race.black and race is not Race.unknown and vkorc1_2255 is GenoVKORC1_2255.t_t:
        return GenoVKORC1_1639.a_a

    # If Race is not "Black or African American" or "Missing or Mixed Race"
    # and rs2359612='C/T' then impute rs9923231='A/G'
    if race is not Race.black and race is not Race.unknown and vkorc1_2255 is GenoVKORC1_2255.c_t:
        return GenoVKORC1_1639.a_g

    # If rs9934438='C/C' then impute rs9923231='G/G'
    if vkorc1_1173 is GenoVKORC1_1173.c_c:
        return GenoVKORC1_1639.g_g

    # If rs9934438='T/T' then impute rs9923231='A/A'
    if vkorc1_1173 is GenoVKORC1_1173.t_t:
        return GenoVKORC1_1639.a_a

    # If rs9934438='C/T' then impute rs9923231='A/G'
    if vkorc1_1173 is GenoVKORC1_1173.c_t:
        return GenoVKORC1_1639.a_g

    # If Race is not "Black or African American" or "Missing or Mixed Race"
    # and rs8050894='G/G' then impute rs9923231='G/G'
    if race is not Race.black and race is not Race.unknown and vkorc1_1542 is GenoVKORC1_1542.g_g:
        return GenoVKORC1_1639.g_g

    # If Race is not "Black or African American" or "Missing or Mixed Race"
    # and rs8050894='C/C' then impute rs9923231='A/A'
    if race is not Race.black and race is not Race.unknown and vkorc1_1542 is GenoVKORC1_1542.c_c:
        return GenoVKORC1_1639.a_a

    # If Race is not "Black or African American" or "Missing or Mixed Race"
    # and rs8050894='C/G' then impute rs9923231='A/G'
    if race is not Race.black and race is not Race.unknown and vkorc1_1542 is GenoVKORC1_1542.c_g:
        return GenoVKORC1_1639.a_g

    return GenoVKORC1_1639.unknown


def parse_genotype_VKORC1_1639(s, race, vkorc1_2255, vkorc1_1173, vkorc1_1542):
    """
    Parse 'VKORC1 -1639 consensus' column in the csv and return GenoVKORC1_1639 enum

    :param s: input string [A/A', nan, 'A/G', 'G/G']
    :return: GenoVKORC1_1639 enum
    """
    geno = GenoVKORC1_1639.unknown
    s = clean_value(s)
    if s == "a/a":
        geno = GenoVKORC1_1639.a_a
    elif s == "a/g":
        geno = GenoVKORC1_1639.a_g
    elif s == "g/g":
        geno = GenoVKORC1_1639.g_g

    if geno == GenoVKORC1_1639.unknown:
        geno = impute_genotype_VKORC1_1639(race, vkorc1_2255, vkorc1_1173, vkorc1_1542)

    return geno
