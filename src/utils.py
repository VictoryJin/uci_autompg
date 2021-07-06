import pandas as pd
from pathlib import Path

CUR_PATH = Path.cwd()


def import_dataset(offline=True):
    """Imports and cleans autompg dataset

    Parameters:
        offline (bool): whether the data should be imported from offline or directly from uci url
    Returns:
        pandas dataframe of autompg with missing values and origin converted
    """
    colnames = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'year', 'origin', 'name']

    try:
        df = pd.read_csv(CUR_PATH.parent / 'data' / 'auto-mpg.data',
                         delim_whitespace=True,
                         names=colnames,
                         na_values='?')
    except FileNotFoundError:
        print('File not found under `data/`, importing from url')
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'
        df = pd.read_csv(url, delim_whitespace=True, names=colnames, na_values='?')

    df['origin'] = df['origin'].map({1: 'USA', 2: 'Europe', 3: 'Japan'})
    return df
