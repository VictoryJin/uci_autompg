import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from statsmodels.stats.diagnostic import normal_ad
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson

from .utils import get_column_by_type

#TODO: Wrap functions in class

def plot_prediction_comparison(y_test, y_pred):
    """Plots performance of linear model based on predicted vs. true values
    
    For validating linear relationships between target and independent variable. 
    If the linear relatioship doesn't hold, then a quadratic term or cubic term should be tested.
    """
    
    a = plt.axes(aspect='equal')
    plt.scatter(y_test, y_pred)
    plt.xlabel("True Values [MPG]")
    plt.ylabel("Predictions [MPG]")
    lims = [0, y_test.max()*1.1]
    plt.xlim(lims)
    plt.ylim(lims)
    plt.plot(lims, lims, color='black')
    print(f"Mean Squared Error from model is {mean_squared_error(y_test, y_pred)}")
    return


def plot_error_distribution(y_test, y_pred):
    """Simple plot of error distribution"""
    error = y_test - y_pred
    plt.hist(error, bins=25)
    plt.xlabel('Prediction Error [MPG]')
    plt.ylabel('Count')
    return


def check_normal_errors(y_test, y_pred, p_threshold=0.05, plot=True):
    """Checks for normality in error distribution" via the Anderson-Darling test"""
    
    residuals = y_test - y_pred
    _, p = normal_ad(residuals)
    
    if p < p_threshold:
        print("Error does not satisfy normality assumption")
    else:
        print("Error satisfies normality assumption")
        
    if plot:
        sns.distplot(residuals)
        plt.show()
    return


def _calculate_vif(X, cols, vif_thresh):
    """Calculates variance inflation factor from only numerical columns"""
    
    # Calculate variance inflation factor for all features
    variables = np.arange(X.shape[1])
    c = X[cols[variables]].values
    vifs = [variance_inflation_factor(c, ix) for ix in np.arange(c.shape[1])]
    for i, vif in enumerate(vifs):
        print(f"{list(X.columns)[i]}: {vif}")
    return
        

def check_multicollinearity(model, X, y, plot=True, vif_thresh=100):
    """Comprehensive check for multicollinearity, or the assumptions that the features
       are not correlated with one another. 
       
       Removes columns above vif_threshold iteratively and returns final dataframe
    """
    # Get all numeric columns
    X_cp = get_column_by_type(X, object, exclude=True)
    cols = X_cp.columns
    
    if plot:
        sns.heatmap(X.corr(), annot=True)
        plt.show()
    
    _calculate_vif(X_cp, cols=cols, vif_thresh=vif_thresh)
    print()
    variables = np.arange(X_cp.shape[1])
    dropped=True
    while dropped:
        dropped=False
        c = X_cp[cols[variables]].values
        vif = [variance_inflation_factor(c, ix) for ix in np.arange(c.shape[1])]

        maxloc = vif.index(max(vif))
        if max(vif) > vif_thresh:
            print('dropping \'' + X_cp[cols[variables]].columns[maxloc] + '\' at index: ' + str(maxloc))
            variables = np.delete(variables, maxloc)
            dropped=True

    print('Remaining variables:')
    print(X_cp.columns[variables])
    return X_cp[cols[variables]]


def check_autocorrelation(y_pred, y_test):
    """Checks for autocorrelation based on Durbin-Watson test
    
    Durbin-Watson: https://en.wikipedia.org/wiki/Durbin-Watson_statistic
    """
    dw = durbin_watson(y_pred - y_test)
    print(f"Durbin-Watson: {dw}")
    
    if dw < 1.5:
        print("Positive autocorrelation")
    elif dw > 2.5:
        print("Negative autocorrealtion")
    else:
        print("Little to no autocorrelation")
    return


def check_homoscedasticity(y_pred, y_test):
    """Checks for assumption that errors have constant variance by plotting the residuals"""
    residuals = pd.DataFrame({'col': y_pred - y_test})
    
    ax = plt.subplot(111)
    plt.scatter(x=residuals.index, y=residuals['col'], alpha=0.5)
    plt.plot(np.repeat(0, len(residuals)))
    plt.show()
    return