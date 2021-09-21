# Overview

Sources for CS234 Project - Estimation of the Warfarin Dose.

[Paper](https://github.com/asyrovprog/cs234-19-project/blob/master/CS234_Paper.pdf)


## FILES

- `/data` - contains provided warfarin.csv dataset and support files
    - **appx.pdf**: appendix file providing the context
    - **metadata.xls**: meta data describing the columns of the data set
    - **warfarin.csv**: original dataset with 5700 patient records
- `results` - where run results and plots are stored
- `clinical_dose.py` - subclass of `Recommender` with implementation of Warfarin Clinical Dosing Algorithm
- `config.py` - configuration classes for algorithms.
- `constant.py` - define constants.
- `ensemble_majority3.py` - subclass of `Recommeder` with implementation of majority vote ensemble algorithm
- `evaluation.py` - utilities for evaluating algorithms.
- `feature.py` - define all enums for features
- `fixed_dose.py` - subclass of `Recommender` with implementation of fixed dose algorithm
- `lasso_bandit.py` - subclass of `Recommeder` with implementation of Lasso bandit algorithm
- `lin_ucb.py` - subclass of `Recommender` with implementation of LinUCB algorithm (disjoint).
- `patient.py` - encapsulate all info about a patient
- `plotting.ipynb` - jupyter notebook to generate plots from a result set from a previous run
- `preprocess.py` - handles all pre-processing of the patient data
- `recommender.py` - abstract `Recommender` class to represent a recommendation model
- `requirements.txt` - for installing required libraries
- `tree_heuristic.py` - subclass of `Recommender` with implementation of DTree algorithm.
- `util.py` - utilities to load and preprocess warfarin dataset
- `warfarin.py` - the `main` program to run Warfarin dosage recommendations

## USAGE
### Run Warfarin Dose Recommender
#### General command template:
```
python warfarin.py --algo=[algo_names] --iter=[iterations] --train_ratio=[training set ratio]
```

- `[algo_names]`: `all` for running all models OR one of `fixed_dose`, `clinical_dose`, `linucb_disjoint`. 
    Default is `fixed_dose`.
- `[iterations]`: Number of iterations to run the experiments through the entire data set. Each iteration will 
    run on a randomly shuffled permutation of the dataset. Default is `1` for single iteration.
- `[training set ratio]`: Ratio of the data set used for training. The rest of the data set is used for test set.
    Default is `0.8` for an 80-20 training/testing split.

#### Examples:
- Run Fixed Dose recommendation (baseline 1) for 1 (default) iteration 
with 80/20 (default) training/testing split:
```
$ python warfarin.py --algo=fixed_dose
```
- Run Warfarin Clinical Dosing Algorithm recommendation (baseline 2) 
for 5 iterations with 80/20 (default) training/testing split::
```
$ python warfarin.py --algo=clinical_dose --iter=5
```
- Run LinUCB Disjoint recommendation for 1 (default) iteration 
with 50/50 training/testing split:
```
$ python warfarin.py --algo=linucb_disjoint --train_ratio=.5
```
- Run ALL models for 10 iterations with 70/30 training/testing split:
```
$ python warfarin.py --algo=all --iter=10 --train_ratio=0.7
```

### Generate Plots from Result Set
```
jupyter notebook
```
- Launch Jupyter notebook
- open `plotting.ipynb` and run the cells


## RESOURCES
  1. [Schedule](https://docs.google.com/document/d/1vIYf-HFQKeuH0-SNvdXx2ylfTErejZMM8p4-wouhuYw/edit?ts=5c69e320)
  2. [Project Page](http://web.stanford.edu/class/cs234/project.html)
  3. [Default Project Page](http://web.stanford.edu/class/cs234/default_project/index.html)

## REFERENCES
  1. [A Contextual-Bandit Approach to Personalized News Article Recommendation](https://arxiv.org/abs/1003.0146)
  2. [Contextual Bandits with Linear Payoff Functions](http://proceedings.mlr.press/v15/chu11a/chu11a.pdf)
  3. [Online Decision-Making with High-Dimensional Covariates](http://web.stanford.edu/~bayati/papers/lassoBandit.pdf)
  4. [A Practical Method for Solving Contextual Bandit Problems Using Decision Trees](https://arxiv.org/pdf/1706.04687.pdf)
