from constant import *


class ConfigFixedDose:

    def __init__(self):
        self.algo_name = "FixedDose"

        # output config
        self.output_path = "results/{}/".format(self.algo_name)
        self.log_path = self.output_path + "log.txt"
        self.regret_plot_output = self.output_path + "regret.png"
        self.payoff_plot_output = None
        self.cfinterval_plot_output = None

        # parameters for the model
        self.fixed_dose = DOSE_MED


class ConfigClinicalDose:

    def __init__(self):
        self.algo_name = "ClinicalDose"

        # output config
        self.output_path = "results/{}/".format(self.algo_name)
        self.log_path = self.output_path + "log.txt"
        self.regret_plot_output = self.output_path + "regret.png"
        self.payoff_plot_output = None
        self.cfinterval_plot_output = None


class ConfigLinUCBDisjoint:

    def __init__(self):
        self.algo_name = "LinUCBDisjoint"

        # output config
        self.output_path = "results/{}/".format(self.algo_name)
        self.log_path = self.output_path + "log.txt"
        self.regret_plot_output = self.output_path + "regret.png"
        self.payoff_plot_output = self.output_path + "payoff.png"
        self.cfinterval_plot_output = self.output_path + "cfinterval.png"

        # parameters for the model
        self.actions = [DOSE_LOW, DOSE_MED, DOSE_HIGH]
        self.alpha = 0.01
        self.feature_count = 134  # this must match actual feature count


class ConfigTreeHeuristic:

    def __init__(self):
        self.algo_name = "TreeHeuristic"

        # output config
        self.output_path = "results/{}/".format(self.algo_name)
        self.log_path = self.output_path + "log.txt"
        self.regret_plot_output = self.output_path + "regret.png"
        self.payoff_plot_output = self.output_path + "payoff.png"
        self.cfinterval_plot_output = self.output_path + "cfinterval.png"

        self.num_arms = 3
        self.tree_depth = 4
        self.criterion = "gini"
        self.alternative_features = True

def get_config(algo_name):
    if algo_name == "fixed_dose":
        return ConfigFixedDose()
    elif algo_name == "clinical_dose":
        return ConfigClinicalDose()
    elif algo_name == "linucb_disjoint":
        return ConfigLinUCBDisjoint()
    elif algo_name == "tree_heuristics":
        return ConfigTreeHeuristic()
