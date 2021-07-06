# Introduction

Quick practice to data analytics, feature engineering, model training/comparison, validations, etc.

# TODOs
Part of the goal for this exercise is to create a reusable data pipeline. After importing the dataset, it would automatically feature engineer the columns and test using a custom series of models. This requires the following functions:
* Automatic feature engineering based on column types
    * normalization, categorical expansion, imputation strategies
* Creates model files
* Takes in model file and generates custom reports/plots for easy comparison
    * This checks for prediction error, overfitting, Mean absolute error (if applicable), AUC, AP
* Model interpretability