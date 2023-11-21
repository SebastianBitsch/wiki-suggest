import networkx as nx
from itertools import count


K = nx.karate_club_graph()

# get unique clubs
groups = set(nx.get_node_attributes(K,'club').values())
mapping = dict(zip(sorted(groups),count()))
nodes = K.nodes()
colors = [mapping[K.nodes[n]['club']] for n in nodes]

#The function take a networkX Graph and a partitioning as inputs and return the modularity
# Define the function to compute modularity
def compute_modularity(K, partition):
    # Get the total number of edges in the graph
    m = K.number_of_edges()
    
    # Initialize the modularity
    Q = 0
    
    # Loop through each community in the partition
    for community in set(partition.values()):
        # Get the nodes in the community
        nodes = [n for n in K.nodes if partition[n] == community]
        
        # Get the number of edges in the community
        ec = sum([1 for (u, v) in K.edges(nodes) if partition[u] == partition[v]])
        
        # Get the sum of the degrees of the nodes in the community
        degc = sum([K.degree[node] for node in nodes])
        
        # Compute the modularity contribution of the community
        qc = ec / m - (degc / (2 * m)) ** 2
        
        # Add the modularity contribution of the community to the total modularity
        Q += qc
    
    return Q

# Define the partition based on the "club" attribute
partition = {node: K.nodes[node]["club"] for node in K.nodes}
#print(partition)

# Compute the modularity of the Karate club split partitioning
Q = compute_modularity(K, partition)

mr_hi_nodes = [k for k, v in partition.items() if v == 'Mr. Hi']
officer_nodes = [k for k, v in partition.items() if v == 'Officer']

# partition_lib = [set(mr_hi_nodes), set(officer_nodes)]
# Q4 = nx.community.modularity(K, partition_lib)
# print(f'The difference is {Q-Q4}')






