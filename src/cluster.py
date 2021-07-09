"""Used to cluster similar words and print out result for utils.cluster_fuzz method"""

from fuzzywuzzy import fuzz

class Node:
    """This Node class allows us to sort variables by their frequency. Each unique name is weighted based on the frequency
    """
    def __init__(self, name, freq):
        self.name = name
        self.freq = freq
        
    def __lt__(self, other):
        return self.freq < other.freq
    
    def __eq__(self, other):
        return self.freq == other.freq
    
    def __gt__(self, other):
        return self.freq > other.freq
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return '{:.0f} {}'.format(self.freq, self.name)


class Link:
    """Used to instantiate one link per each variable combination, based on fuzz.ratio score"""
    def __init__(self, source, target, ratio):
        self.source = source
        self.target = target
        self.ratio = ratio
    
    def __lt__(self, other):
        return self.ratio < other.ratio
    
    def __eq__(self, other):
        return self.ratio == other.ratio
    
    def __gt__(self, other):
        return self.ratio > other.ratio
    
    def __hash__(self):
        return hash(self.source.name + " " + self.target.name)
    
    def __str__(self):
        return '{} <- {:.0f} -> {}'.format(self.source.name, self.ratio, self.target.name)
    
    
class Cluster:
    """Nodes are added to a cluster when one of their LInks has a fuzz.ratio above ratio_threshold"""
    def __init__(self, node):
        self.nodes = {node}
        self.maxNode = node
        self.name = node.name
        
    def add(self, node):
        self.nodes.add(node)
        if (node > self.maxNode):
            self.maxNode = node
            
    def join(self, other):
        for node in other.nodes:
            self.add(node)
    
    def __lt__(self, other):
        return self.maxNode.freq < other.maxNode.freq
    
    def __gt__(self, other):
        return self.maxNode.freq > other.maxNode.freq
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return f'{len(self.nodes)} {self.name}: {self.maxNode.freq} | CLUSTER: {[(fuzz.ratio(self.name, node.name),node.name) for node in self.nodes if not node.name==self.name]}'
