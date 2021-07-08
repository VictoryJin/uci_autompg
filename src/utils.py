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
        df = pd.read_csv(CUR_PATH / 'data' / 'auto-mpg.data',
                         delim_whitespace=True,
                         names=colnames,
                         na_values='?')
    except FileNotFoundError:
        print('File not found under `data/`, importing from url')
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'
        df = pd.read_csv(url, delim_whitespace=True, names=colnames, na_values='?')

    df['origin'] = df['origin'].map({1: 'USA', 2: 'Europe', 3: 'Japan'})
    return df


def lazy_ldist(word1, word2):
    """Recomputes the distance for recursively via insert, delete, replace
    Reference: https://en.wikipedia.org/wiki/Levenshtein_distance#Recursive
    
    >>> lazy_ldist('test_insertion', 'test_insertion_extra')
    6
    >>> lazy_ldist('test_deletion', 'test')
    9
    >>> lazy_ldist('asdf', 'dsdf')
    1
    >>> lazy_ldist('test_replacement', 'xesd_replacement')
    # Should be 2, but takes infinite due insertion
    
    Parameters:
        wd1, wd2 (str): first and second string
    """
    assert isinstance(word1, str) & isinstance(word2, str)
    
    # Always enforce 
    
    lword1, lword2 = len(word1), len(word2) 
    # Base case 1: if either word is empty then distance is the number of characters in t
    if lword1==0:
        return lword2
    if lword2==0:
        return lword1
    
    # Base case 2: if characters are the same, ignore
    if word1[0]==word2[0]:
        return lazy_ldist(word1[1:], word2[1:])
    
    # If not, recursively try insertion, deletion, and substitution
    return 1 + min(lazy_ldist(word2[0]+word1, word2),     # insertion
                   lazy_ldist(word1[1:], word2),          # deletion
                   lazy_ldist(word2[0]+word1[1:], word2)) # replacement