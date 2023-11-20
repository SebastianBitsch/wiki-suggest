import numpy as np
import networkx as nx

def edge_list(G):

    # Get the edge list with weights
    edge_list_with_weights = [(u, v, d['weight']) for u, v, d in G.edges(data=True)]

    # Print the edge list
    return edge_list_with_weights


def adjacency_matrix(edge_list):
    
    # construct the pairwise distance matrix
    #A = pairwise_distances(X, metric='euclidean')

    # Number of nodes (assuming nodes are labeled from 0 to n-1)
    n_nodes = len(edge_list)

    # Constructing the similarity matrix 
    A = np.zeros((n_nodes, n_nodes))

    for node1, node2, weight in edge_list:
        A[node1, node2] = weight
        A[node2, node1] = weight  
    
    return A


# spectral clustering with the given epsilon, the distance critera for two pooints to be considered in the same cluster
def spectral_clustering(G):
    
    edge_list_G = edge_list(G)
    
    n = len(edge_list_G)
    
     # create the similarity matrix
    A = adjacency_matrix(edge_list_G)
    
    # Compute the sum of weights for each node
    degree_sums = np.sum(A, axis=1)

    # Create the degree matrix as a diagonal matrix
    D = np.diag(degree_sums)
    
    # create the normalized Laplacian matrix
    L = np.linalg.pinv(D) @ (D -  A)
    
    # computing the eigenvector for the second-smallest eigenvalue
    eigval_sorted = np.linalg.eig(L)[0].argsort() # indices of sorted eigenvalues
    eigvecs = np.linalg.eig(L)[1] # matrix of eigenvectors
    z_eigvec = eigvecs[:,eigval_sorted][:,1] # eigenvec w.r.t. second smallest eigenvalue
    
    z_eigvec[z_eigvec >= 0] = 1
    z_eigvec[z_eigvec < 0] = 0
    
    return z_eigvec



# Create an undirected graph
G = nx.Graph()

# Add nodes, you can add as many as you need
G.add_nodes_from([1, 2, 3, 4, 5])

# Add edges with weights
# The tuple is (node1, node2, weight)
G.add_weighted_edges_from([(1, 2, 1.5), (1, 3, 2.0), 
                           (2, 4, 2.5), (3, 4, 1.0), 
                           (4, 5, 3.0), (1, 5, 2.5)])


print(spectral_clustering(G))