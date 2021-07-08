

#Threshold to use for clustering.  The variable with the highest ROC from each cluster will be returned.
corr_thresh = 0.4
corr_df = corr_trdf

# This Node class will allow us to sort variables by their ROC values
class Node:
    def __init__(self, name, roc):
        self.name = name
        self.roc = roc
        
    def __lt__(self, other):
        return self.roc < other.roc
    
    def __eq__(self, other):
        return self.roc == other.roc
    
    def __gt__(self, other):
        return self.roc > other.roc
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return '{:.3f} {}'.format(self.roc, self.name)

# Assume existence of rocDict from above.
nodeDict = {}
for nodeName in rocDict.keys():
    nodeDict[nodeName] = Node(nodeName, rocDict[nodeName])

# There will be one Link for every pair of variables.
class Link:
    def __init__(self, source, target, corr):
        self.source = source
        self.target = target
        self.corr = corr
    
    def __lt__(self, other):
        return self.corr < other.corr
    
    def __eq__(self, other):
        return self.corr == other.corr
    
    def __gt__(self, other):
        return self.corr > other.corr
    
    def __hash__(self):
        return hash(self.source.name + " " + self.target.name)
    
    def __str__(self):
        return '{} <- {:.3f} -> {}'.format(self.source.name, self.corr, self.target.name)
    

linkSet = set()
for i in range(len(corr_df.columns) - 1):
    for j in range(i+1, len(corr_df.columns)):
        link_corr = corr_df.iloc[i,j]
        link_source = nodeDict[corr_df.columns[i]]
        link_target = nodeDict[corr_df.columns[j]]
        linkSet.add(Link(link_source, link_target, link_corr))
        
#Nodes will be added to a Cluster when one of their Links has a corr above the corr_thresh.
class Cluster:
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
        return self.maxNode.roc < other.maxNode.roc
    
    def __gt__(self, other):
        return self.maxNode.roc > other.maxNode.roc
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return '{} {} | {:.3f} {}'.format(len(self.nodes), self.name, self.maxNode.roc, self.maxNode.name)


clusterSet = set()
#Start with each node in its own cluster.
for nodeName in nodeDict.keys():
    clusterSet.add(Cluster(nodeDict[nodeName]))
    
# Iterate through list of links, sorted in descending order of correlation, and do clustering.
for link in sorted(linkSet, reverse=True):
    if(link.corr < corr_thresh):
        break
    sourceCluster = None
    for cluster in clusterSet:
        if(link.source in cluster.nodes):
            sourceCluster = cluster
            break
    targetCluster = None
    for cluster in clusterSet:
        if(link.target in cluster.nodes):
            targetCluster = cluster
            break
    if(not(sourceCluster is targetCluster)):
        sourceCluster.join(targetCluster)
        clusterSet.remove(targetCluster)
    
print(len(clusterSet))

# Print out list of surviving clusters
print('Variables for correlation threshold {}'.format(corr_thresh))
print('---------------------------------------')
for cluster in sorted(clusterSet, reverse=True):
    print(cluster)