from recommender import *
import logging


class Majority3Recommender(Recommender):

    def get_features(self, patient):
        """
        Algorithm-specific feature processing
        Dummy function, the returned features are not used in recommend function at all.
        But this will help us distinguish features not used vs features is None (missing data)

        :param patient: patient data
        :return: feature vector for the given patient
        """
        return 1

    def recommend(self, features, eval_results, iter, patient_idx):
        """
        Recommend an action based on majority voting. Use fixed dose for tie breaking.

        returns:
            action: An integer representing the selected action.
            payoff: None
            conf_interval: None
        """
        action = self.config.fixed_dose

        if eval_results is not None:
            arms = [0] * 3
            for m in range(len(eval_results.models)):
                model = eval_results.models[m]
                # ensemble panel votes
                if model.config.algo_name in self.config.ensemble_list:
                    arms[eval_results.actions[m][iter][patient_idx]] += 1

            mx = max(arms)  # get majority vote
            action = arms.index(mx) if mx > 1 else self.config.fixed_dose

        return action, None, None
