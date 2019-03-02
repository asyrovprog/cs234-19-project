# Impute some missing genome type based on
# section s4 of appx.pdf
import pandas as pd

data = pd.read_csv("data/warfarin.csv")

"""
u'VKORC1 genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T',
u'VKORC1 QC genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T',
u'VKORC1 genotype: 497T>G (5808); chr16:31013055; rs2884737; A/C',
u'VKORC1 QC genotype: 497T>G (5808); chr16:31013055; rs2884737; A/C',
u'VKORC1 genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G',
u'VKORC1 QC genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G',
u'VKORC1 genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G',
u'VKORC1 QC genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G',
u'VKORC1 genotype: 3730 G>A (9041); chr16:31009822; rs7294;  A/G',
u'VKORC1 QC genotype: 3730 G>A (9041); chr16:31009822; rs7294;  A/G',
u'VKORC1 genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G',
u'VKORC1 QC genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G',
u'VKORC1 genotype: -4451 C>A (861); Chr16:31018002; rs17880887; A/C',
u'VKORC1 QC genotype: -4451 C>A (861); Chr16:31018002; rs17880887; A/C',
"""

target = data["VKORC1 genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T"]

cond = (
    (data["Race"] != "Black or African American") &
    (data["Race"] != "Missing or Mixed Race") & 
    (data["VKORC1 genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G"] == "C/C"))
target[cond] = "G/G"

cond = (
    (data["Race"] != "Black or African American") &
    (data["Race"] != "Missing or Mixed Race") & 
    (data["VKORC1 genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G"] == "T/T"))
target[cond] = "A/A"

cond = (
    (data["Race"] != "Black or African American") &
    (data["Race"] != "Missing or Mixed Race") & 
    (data["VKORC1 genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G"] == "C/T"))
target[cond] = "A/G"

cond = data["VKORC1 genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G"] == "G/G"
target[cond] = "G/G"

cond = data["VKORC1 genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G"] == "T/T"
target[cond] = "A/A"

cond = data["VKORC1 genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G"] == "C/T"
target[cond] = "A/G"

cond = (
    (data["Race"] != "Black or African American") &
    (data["Race"] != "Missing or Mixed Race") & 
    (data["VKORC1 genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G"] == "G/G"))
target[cond] = "G/G"

cond = (
    (data["Race"] != "Black or African American") &
    (data["Race"] != "Missing or Mixed Race") & 
    (data["VKORC1 genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G"] == "C/C"))
target[cond] = "A/A"

cond = (
    (data["Race"] != "Black or African American") &
    (data["Race"] != "Missing or Mixed Race") & 
    (data["VKORC1 genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G"] == "C/G"))
target[cond] = "A/G"

data.to_csv("data/warfarin_imputed_missing.csv", index=False)

