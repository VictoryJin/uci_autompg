# Introduction

Quick basic practice to data science workflow. Part of the goal for this exercise is to have a quick reference for data science methods and to create a reusable data science framework. This repo demonstrates the following
#### Data Science
* Data Analysis
* Feature Engineering
* Short Text Analysis
* Long text analysis (unavailable via the UCI dataset)
* Model development
    * Supervised methods - Linear model
    * Unsupervised methods
    * Neural Networks
    * Model interpretability  

#### MLOps
* Utility libraries and pipeline development under `src`
* Operationalization
* Dashboarding

# TODOs
After importing the dataset, it would automatically feature engineer the columns and test using a custom series of models. This requires the following functions:
* Automatic feature engineering based on column types
    * normalization, categorical expansion, imputation strategies
* Creates model files
* Takes in model file and generates custom reports/plots for easy comparison
    * This checks for prediction error, overfitting, Mean absolute error (if applicable), AUC, AP
* Model interpretability

# Logs
* **7/5**: Define project skeleton, create import function w/ basic preprocessing
* **7/6**: Basic EDA via pairplot visualization. Additional preprocessing/feature engineering.
* **7/9**: Fuzzy matching and implementation into import pipeline. Train baseline model
* **7/13**: OLS Assumptions testing, as referenced from [JeffMaculuso's Cookbook](https://github.com/JeffMacaluso/Cookbook/blob/master/MachineLearning/Miscellaneous.py)
* **7/XX**: Implement train/metric report pipeline through scikit-learn, xgboost, catboost. Comparisons for each model
* **7/XX**: Train neural network, encoding methodologies, compare performance. 
* **7/XX**: Recreate [paper1](http://reports-archive.adm.cs.cmu.edu/anon/2004/CMU-CS-04-134.pdf) & [paper2](https://digitalcommons.unl.edu/dissertations/AAI3159564/).  

Finish