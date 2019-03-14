import enum
from constant import *

"""
warfarin.csv contains 63 titled columns plus 3 empty columns at the end. 
Below is the list of the 63 titled columns:

* indicates columns we use
------------------------------------------------
PharmGKB Subject ID
Gender *
Race *
Ethnicity
Age *
Height (cm) *
Weight (kg) *
Indication for Warfarin Treatment *
Comorbidities
Diabetes *
Congestive Heart Failure and/or Cardiomyopathy *
Valve Replacement *
Medications *
Aspirin *
Acetaminophen or Paracetamol (Tylenol) *
Was Dose of Acetaminophen or Paracetamol (Tylenol) >1300mg/day *
Simvastatin (Zocor) *
Atorvastatin (Lipitor) *
Fluvastatin (Lescol)
Lovastatin (Mevacor)
Pravastatin (Pravachol)
Rosuvastatin (Crestor)
Cerivastatin (Baycol)
Amiodarone (Cordarone)
Carbamazepine (Tegretol)
Phenytoin (Dilantin)
Rifampin or Rifampicin
Sulfonamide Antibiotics
Macrolide Antibiotics
Anti-fungal Azoles
"Herbal Medications, Vitamins, Supplements"
Target INR *
Estimated Target INR Range Based on Indication (maybe?)
Subject Reached Stable Dose of Warfarin *
Therapeutic Dose of Warfarin
INR on Reported Therapeutic Dose of Warfarin (maybe?)
Current Smoker *
Cyp2C9 genotypes
Genotyped QC Cyp2C9*2
Genotyped QC Cyp2C9*3
Combined QC CYP2C9
VKORC1 genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T
VKORC1 QC genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T
VKORC1 genotype: 497T>G (5808); chr16:31013055; rs2884737; A/C
VKORC1 QC genotype: 497T>G (5808); chr16:31013055; rs2884737; A/C
VKORC1 genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G
VKORC1 QC genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G
VKORC1 genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G
VKORC1 QC genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G
VKORC1 genotype: 3730 G>A (9041); chr16:31009822; rs7294;  A/G
VKORC1 QC genotype: 3730 G>A (9041); chr16:31009822; rs7294;  A/G
VKORC1 genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G
VKORC1 QC genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G
VKORC1 genotype: -4451 C>A (861); Chr16:31018002; rs17880887; A/C
VKORC1 QC genotype: -4451 C>A (861); Chr16:31018002; rs17880887; A/C
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

class Gender(enum.Enum):
    """
    field name: 'Gender'
    unique values: 'male', 'female', nan
    """
    unknown = VAL_UNKNOWN
    male = 1
    female = 2


class Race(enum.Enum):
    """
    field name: 'Race'
    unique values: 'White', 'Asian', 'Unknown',
                    'Black or African American'
    """
    unknown = VAL_UNKNOWN
    asian = 1
    white = 2
    black = 3
    other = 4


class AgeGroup(enum.Enum):
    """
    field name: 'Age'
    unique values: '60 - 69', '50 - 59', '40 - 49', '70 - 79', '30 - 39', '80 - 89',
       '90+', '20 - 29', '10 - 19', nan
    """
    unknown = VAL_UNKNOWN
    zero = 0
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9


class Indication(enum.Enum):
    """
    field name: 'Indication for Warfarin Treatment'
    unique values: nan, '4', '3', '1; 2', '6; 8', '6', '2', '8', '3; 8', '1',
       '3; 4; 6', '3; 6', '7; 8', '4; 8', '3; 4', '3; 6; 8', '3; 7; 8',
       '3; 6; 7', '4; 6; 8', '7', '3; 2', '5', '3; 5', '3; 4; 8', '4; 7',
       '1; 3; 8', '3; 7', '1 or 2', '2; 6', '5; 8', '3; 4; 7; 8',
       '3; 4; 7', '4; 7; 8', '1; 2; 8', '4; 6', '3; 4; 6; 8', '1; 2; 3',
       '4; 3', '6; 5', '1; 6', '2; 8', '1;2', '5; 6', '1; 3',
       '3; 4; 6; 7; 8', '1; 8', '2; 3; 8', '4;6', '1; 3; 4; 8', '2; 3',
       '4; 5', '1; 2; 5; 8', '1,2'
    """
    unknown = VAL_UNKNOWN
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8


class BinaryFeature(enum.Enum):
    """
    field names:
    'Diabetes', 'Congestive Heart Failure and/or Cardiomyopathy', 'Valve Replacement', 'Aspirin',
    'Acetaminophen or Paracetamol (Tylenol)', 'Was Dose of Acetaminophen or Paracetamol (Tylenol) >1300mg/day',
    'Simvastatin (Zocor)', 'Atorvastatin (Lipitor)', 'Fluvastatin (Lescol)', 'Lovastatin (Mevacor)',
    'Pravastatin (Pravachol)', 'Rosuvastatin (Crestor)', 'Cerivastatin (Baycol)', 'Amiodarone (Cordarone)',
    'Carbamazepine (Tegretol)', 'Phenytoin (Dilantin)', 'Rifampin or Rifampicin', 'Sulfonamide Antibiotics',
    'Macrolide Antibiotics', 'Anti-fungal Azoles', "Herbal Medications, Vitamins, Supplements",
    'Subject Reached Stable Dose of Warfarin', 'Current Smoker'

    unique values: nan, 0, 1
    """
    unknown = VAL_UNKNOWN
    false = 0
    true = 1


class GenoCYP2C9(enum.Enum):
    """
    field name: 'CYP2C9 consensus'
    unique values: '*2/*3', '*3/*3', '*1/*1', '*1/*3', nan, '*2/*2', '*1/*2',
       '*1/*14', '*1/*13', '*1/*11', '*1/*5', '*1/*6'
    """
    unknown = VAL_UNKNOWN
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    eleven = 11
    twelve = 12
    thirteen = 13
    fourteen = 14


class GenoVKORC1_1639(enum.Enum):
    """
    field name: 'VKORC1 -1639 consensus' (rs9923231)
    unique values: 'A/A', nan, 'A/G', 'G/G'
    """
    unknown = VAL_UNKNOWN
    a_a = 1
    a_g = 2
    g_g = 3


class GenoVKORC1_497(enum.Enum):
    """
    field name: 'VKORC1 497 consensus' (rs2884737)
    unique values: nan, 'G/T', 'T/T', 'G/G'
    """
    unknown = VAL_UNKNOWN
    g_g = 1
    g_t = 2
    t_t = 3


class GenoVKORC1_1173(enum.Enum):
    """
    field name: 'VKORC1 1173 consensus' (rs9934438)
    unique values: nan, 'T/T', 'C/T', 'C/C'
    """
    unknown = VAL_UNKNOWN
    c_c = 1
    c_t = 2
    t_t = 3


class GenoVKORC1_1542(enum.Enum):
    """
    field name: 'VKORC1 1542 consensus' (rs8050894)
    unique values: nan, 'C/C', 'C/G', 'G/G'
    """
    unknown = VAL_UNKNOWN
    c_c = 1
    c_g = 2
    g_g = 3


class GenoVKORC1_3730(enum.Enum):
    """
    field name: 'VKORC1 3730 consensus' (rs7294)
    unique values: nan, 'G/G', 'A/G', 'A/A'
    """
    unknown = VAL_UNKNOWN
    a_a = 1
    a_g = 2
    g_g = 3


class GenoVKORC1_2255(enum.Enum):
    """
    field name: 'VKORC1 2255 consensus' (rs2359612)
    unique values: nan, 'T/T', 'C/T', 'C/C'
    """
    unknown = VAL_UNKNOWN
    c_c = 1
    c_t = 2
    t_t = 3


class GenoVKORC1_4451(enum.Enum):
    """
    field name: 'VKORC1 -4451 consensus' (rs17880887)
    unique values: nan, 'A/C', 'C/C', 'A/A'
    """
    unknown = VAL_UNKNOWN
    a_a = 1
    a_c = 2
    c_c = 3
