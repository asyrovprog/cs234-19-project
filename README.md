# Sources for CS234 Project - Estimation of the Warfarin Dose

## Files:

- `/data` - contains provided warfarin.csv dataset and support files
- `tools.py` - utilities to load and preprocess warfarin dataset
- `baseline_fixed_dose.py` - implementation of fixed dose algorithm
- `baseline_clinical.py` - implementation of Warfarin Clinical Dosing Algorithm
- `baseline_tf.py` - attempt to improve over Clinical Algorithm with tensorflow (this is not required for project)
- `bandit.py` - implementation of bandits.
- `evaluation.py` - utilities for evaluting bandits.

Links:
  1. [Schedule](https://docs.google.com/document/d/1vIYf-HFQKeuH0-SNvdXx2ylfTErejZMM8p4-wouhuYw/edit?ts=5c69e320)
  2. [Project Page](http://web.stanford.edu/class/cs234/project.html)
  3. [Default Project Page](http://web.stanford.edu/class/cs234/default_project/index.html)


TODOS:
- [X] implement "Imputation of VKORC1 SNPs"
- [] add better data preprocessing. Use one-hot encoding for categorical feature, etc.
- [] implement linear bandit