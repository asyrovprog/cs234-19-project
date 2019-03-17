import datetime
from constant import *


class ConfigCommon:
    def __init__(self, output_path):
        # output config
        self.output_path = output_path

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

    def __init__(self, output_path):
        super().__init__(output_path)
        self.algo_name = "FixedDose"

        # parameters for the model
        self.fixed_dose = DOSE_MED


class ConfigClinicalDose(ConfigCommon):

    def __init__(self, output_path):
        super().__init__(output_path)
        self.algo_name = "ClinicalDose"


class ConfigLinUCBDisjoint(ConfigCommon):

    def __init__(self, output_path):
        super().__init__(output_path)
        self.algo_name = "LinUCBDisjoint"

        # parameters for the model
        self.actions = [DOSE_LOW, DOSE_MED, DOSE_HIGH]
        self.alpha = 0.01
        self.feature_count = 134  # this must match actual feature count


class ConfigLinUCBDisjointBasic(ConfigLinUCBDisjoint):

    def __init__(self, output_path):
        super().__init__(output_path)
        self.algo_name = "LinUCBDisjointBasic"

        # parameters for the model
        self.feature_count = 9  # this must match actual feature count

class ConfigTreeHeuristic(ConfigCommon):
    def __init__(self, output_path):
        super().__init__(output_path)
        self.algo_name = "DTree-Alt"
        self.num_arms = 3
        self.tree_depth = 4
        self.min_samples_split = 37
        self.min_samples_leaf = 11
        self.max_leaf_nodes = 4
        self.criterion = "gini"
        self.feature_set = "exdended"

class ConfigTreeHeuristicBasic(ConfigTreeHeuristic):
    def __init__(self, output_path):
        super().__init__(output_path)
        self.algo_name = "DTree"
        self.feature_set = "clinical"
        self.tree_depth = 4


class ConfigLasso(ConfigCommon):

    def __init__(self, output_path):
        super().__init__(output_path)
        self.algo_name = "Lasso"

        self.num_arms = 3
        # At the beginning we force sample each arm 20 times and this will be the only
        # time we force sample.
        self.q = 20
        self.n = 1
        # Include all arms..
        self.h = 10
        self.lambda1 = 1.0
        self.lambda2 = 1.0


def get_config(algo_name, output_path):
    if algo_name == "fixed_dose":
        return ConfigFixedDose(output_path)
    elif algo_name == "clinical_dose":
        return ConfigClinicalDose(output_path)
    elif algo_name == "linucb_disjoint":
        return ConfigLinUCBDisjoint(output_path)
    elif algo_name == "linucb_disjoint_basic":
        return ConfigLinUCBDisjointBasic(output_path)
    elif algo_name == "tree":
        return ConfigTreeHeuristic(output_path)
    elif algo_name == "tree_basic":
        return ConfigTreeHeuristicBasic(output_path)
    elif algo_name == "lasso":
        return ConfigLasso(output_path)
