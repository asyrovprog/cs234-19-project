import datetime
from constant import *


class ConfigCommon:
    def __init__(self):
        # output config
        self.output_path = "results/{}/".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        self.log_path = self.output_path + "log.txt"
        self.regret_plot_output = self.output_path + "regret.png"
        self.payoff_plot_output = self.output_path + "payoff.png"
        self.cfinterval_plot_output = self.output_path + "cfinterval.png"

    def get_regret_filename(self, model, is_training):
        s = "training" if is_training else "testing"
        return f"{self.output_path}{s}_regret_{model}.csv"

    def get_mistake_filename(self, model, is_training):
        s = "training" if is_training else "testing"
        return f"{self.output_path}{s}_mistake_{model}.csv"

    def get_payoff_filename(self, model, is_training):
        s = "training" if is_training else "testing"
        return f"{self.output_path}{s}_payoff_{model}.csv"

    def get_conf_interval_filename(self, model, is_training):
        s = "training" if is_training else "testing"
        return f"{self.output_path}{s}_conf_interval_{model}.csv"


class ConfigFixedDose(ConfigCommon):

    def __init__(self):
        super().__init__()
        self.algo_name = "FixedDose"

        # parameters for the model
        self.fixed_dose = DOSE_MED


class ConfigClinicalDose(ConfigCommon):

    def __init__(self):
        super().__init__()
        self.algo_name = "ClinicalDose"


class ConfigLinUCBDisjoint(ConfigCommon):

    def __init__(self):
        super().__init__()
        self.algo_name = "LinUCBDisjoint"

        # parameters for the model
        self.actions = [DOSE_LOW, DOSE_MED, DOSE_HIGH]
        self.alpha = 0.01
        self.feature_count = 134  # this must match actual feature count


class ConfigTreeHeuristic(ConfigCommon):

    def __init__(self):
        super().__init__()
        self.algo_name = "TreeHeuristic"

        # parameters for the model
        self.num_arms = 3
        self.tree_depth = 3


def get_config(algo_name):
    if algo_name == "fixed_dose":
        return ConfigFixedDose()
    elif algo_name == "clinical_dose":
        return ConfigClinicalDose()
    elif algo_name == "linucb_disjoint":
        return ConfigLinUCBDisjoint()
    elif algo_name == "tree_heuristics":
        return ConfigTreeHeuristic()
