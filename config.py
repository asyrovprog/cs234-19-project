from constant import  *


class ConfigFixedDose:

    def __init__(self):
        self.algo_name = "FixedDose"

        # output config
        self.output_path = "results/{}/".format(self.algo_name)
        self.log_path = self.output_path + "log.txt"
        self.plot_output = self.output_path + "scores.png"

        # parameters for the model
        self.fixed_dose = DOSE_MED


class ConfigClinicalDose:

    def __init__(self):
        self.algo_name = "ClinicalDose"

        # output config
        self.output_path = "results/{}/".format(self.algo_name)
        self.log_path = self.output_path + "log.txt"
        self.plot_output = self.output_path + "scores.png"


class ConfigLinUCBDisjoint:

    def __init__(self):
        self.algo_name = "LinUCBDisjoint"

        # output config
        self.output_path = "results/{}/".format(self.algo_name)
        self.log_path = self.output_path + "log.txt"
        self.plot_output = self.output_path + "scores.png"

        # model and training config

        # parameters for the model
        self.actions = [DOSE_LOW, DOSE_MED, DOSE_HIGH]
        self.alpha = 0.0


def get_config(algo_name):
    if algo_name == "fixed_dose":
        return ConfigFixedDose()
    elif algo_name == "clinical_dose":
        return ConfigClinicalDose()
    elif algo_name == "linucb_disjoint":
        return ConfigLinUCBDisjoint()