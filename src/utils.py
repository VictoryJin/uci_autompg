import pandas as pd
from pathlib import Path
from fuzzywuzzy import fuzz

from .cluster import Node, Edge, Cluster

CUR_PATH = Path.cwd()


def import_dataset(remove_na=True):
    """Imports and cleans autompg dataset

    Parameters:
        remove_na (bool): whether the 6 rows containing NA values should be removed or not
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
    
    # Remove_nas if specified
    if remove_na:
        df = df.dropna()
    
    # Based on `2. Fuzzy Matching.ipynb` - Retrieve model and fix model names based on fuzzy matches
    df['model'] = df['name'].apply(lambda x: x.split(' ')[0])
    
    correct_dict = {
        'chevrolet': ['chevroelt', 'chevy'],
        'toyota' : ['toyouta'],
        'mazda'  : ['maxda'],
        'volkswagen': ['vokswagen', 'vw'],
        'mercedes-benz': ['mercedes']
    }
    for correct_wd in correct_dict.keys():
        df['model'] = df['model'].replace(correct_dict[correct_wd], correct_wd)
    return df


def get_column_by_type(df, dtype, exclude=False):
    """Indexes and returns column by type, or excluded by type"""
    if exclude:
        return df.loc[:, df.dtypes != dtype]
    else:
        return df.loc[:, df.dtypes == dtype]


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


def cluster_fuzz(model_dict, ratio_threshold):
    """Function that clusters similar names based on fuzz.ratio and prints priority word based on frequency. 
    
    Parameters:
        model_dict(dict): dictionary containing model name as key and frequency as value. 
        
    
    """
    nodeDict = {}
    for nodeName in model_dict.keys():
        nodeDict[nodeName] = Node(nodeName, model_dict[nodeName])

    edgeSet = set()
    for i in range(len(model_dict.keys())-1):
        for j in range(i+1, len(model_dict.keys())):
            edge_ratio = fuzz.ratio(list(model_dict)[i], list(model_dict)[j])  # get ratio score
            edge_source = nodeDict[list(model_dict)[i]]                        # define source edge
            edge_target = nodeDict[list(model_dict)[j]]                        # define target edge
            edgeSet.add(Edge(edge_source, edge_target, edge_ratio))

    clusterSet = set()
    #Start with each node in its own cluster.
    for nodeName in nodeDict.keys():
        clusterSet.add(Cluster(nodeDict[nodeName]))

    # Iterate through list of edges, sorted in descending order of correlation, and do clustering.
    for edge in sorted(edgeSet, reverse=True):
        if(edge.ratio < ratio_threshold):
            break
        sourceCluster = None
        for cluster in clusterSet:
            if(edge.source in cluster.nodes):
                sourceCluster = cluster
                break
        targetCluster = None
        for cluster in clusterSet:
            if(edge.target in cluster.nodes):
                targetCluster = cluster
                break
        if(not(sourceCluster is targetCluster)):
            sourceCluster.join(targetCluster)
            clusterSet.remove(targetCluster)

    print(f"There are {len(clusterSet)} clusters")
    print('Variables for correlation threshold {}'.format(ratio_threshold))
    print('---------------------------------------')
    for cluster in sorted(clusterSet, reverse=True):
        print(cluster)