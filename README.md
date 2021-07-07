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

# Logs
* **7/5**: Define project skeleton, create import function w/ basic preprocessing
* **7/6**: Basic EDA via pairplot visualization. Additional preprocessing/feature engineering.
* **7/7 (planned)**: Fuzzy matching and implementation into import pipeline. Train baseline model
* **7/8 (planned)**: Implement train/metric report pipeline through scikit-learn, xgboost, catboost. Comparisons for each model
* **7/9 (planned)**: Train neural network, encoding methodologies, compare performance. 
* **7/11 (planned)**: Recreate [paper1](http://reports-archive.adm.cs.cmu.edu/anon/2004/CMU-CS-04-134.pdf) & [paper2](https://digitalcommons.unl.edu/dissertations/AAI3159564/).  

Finish