# Sources for CS234 Project - Estimation of the Warfarin Dose

## Files:

- `/data` - contains provided warfarin.csv dataset and support files
    - **warfarin.csv**: original dataset with 5700 patient records
    - **warfarin_5528.csv**: removed 172 patients records with 'NA' in "Therapeutic Dose of Warfarin" column 
    - **warfarin_5528_imputed.csv**: imputed missing values in warfarin_5528.csv by running `impute_missing.py`
    - **warfarin_imputed_missing.csv**: imputed missing values in warfarin.csv by running `impute_missing.py`
- `logs` - where log files are located
- `results` - where run results and plots are stored per model
- `v1` - initial implementations
- `warfarin.py` - the `main` program to run Warfarin dosage recommendations
- `recommender.py` - abstract `Recommender` class to represent a recommendation model
- `fixed_dose.py` - subclass of `Recommender` with implementation of fixed dose algorithm
- `clinical_dose.py` - subclass of `Recommender` with implementation of Warfarin Clinical Dosing Algorithm
- `lin_ucb.py` - subclass of `Recommender` with implementation of LinUCB algorithms (disjoint & hybrid).
- `evaluation.py` - utilities for evaluting algorithms.
- `config.py` - configuration classes for algorithms.
- `constant.py` - define constants.
- `impute_missing.py` - standalone script to impute missing data in the source CSV
- `util.py` - utilities to load and preprocess warfarin dataset
- `requirements.txt` - for installing required libraries

## Usage:
### Impute missing data:
* Impute missing data in `data/warfarin_5528.csv` and create new file `data/warfarin_5528_imputed.csv`:
```
$ python impute_missing.py --in_file="warfarin_5528.csv" --out_file="warfarin_5528_imputed.csv"
```
### Run a recommender:
* Fixed Dose recommendation (baseline 1):
```
$ python warfarin.py --algo=fixed_dose
```
* Warfarin Clinical Dosing Algorithm recommendation (baseline 2):
```
$ python warfarin.py --algo=clinical_dose
```
* LinUCB Disjoint recommendation:
```
$ python warfarin.py --algo=linucb_disjoint
```

## Links:
  1. [Schedule](https://docs.google.com/document/d/1vIYf-HFQKeuH0-SNvdXx2ylfTErejZMM8p4-wouhuYw/edit?ts=5c69e320)
  2. [Project Page](http://web.stanford.edu/class/cs234/project.html)
  3. [Default Project Page](http://web.stanford.edu/class/cs234/default_project/index.html)

## References:
  1. [A Contextual-Bandit Approach to Personalized News Article Recommendation](https://arxiv.org/abs/1003.0146)
  2. [Contextual Bandits with Linear Payoff Functions](http://proceedings.mlr.press/v15/chu11a/chu11a.pdf)
  3. [Online Decision-Making with High-Dimensional Covariates](http://web.stanford.edu/~bayati/papers/lassoBandit.pdf)
  4. [A Practical Method for Solving Contextual Bandit Problems Using Decision Trees](https://arxiv.org/pdf/1706.04687.pdf)

## TODOS:
- [X] implement "Imputation of VKORC1 SNPs"
- [X] add better data preprocessing. Use one-hot encoding for categorical feature, etc.
- [X] add model eval logging.
- [X] implement linear bandit
- [X] alternate learning/evaluation approach
- [X] explore feature normalization
- [X] add new feature (BMI instead of height/weight? INR data?)
- [ ] variations of LinUCB (hybrid, SupLin?)
- [ ] implement Lasso bandit
- [ ] export training and testing results to file
- [ ] create combined plots

