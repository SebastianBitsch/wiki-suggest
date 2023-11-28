import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering
import pickle
import glob

def adjacency_matrix(G: nx.Graph, order):
    
    # construct the pairwise distance matrix
    #A = pairwise_distances(X, metric='euclidean')

    # Number of nodes
    n_nodes = G.number_of_nodes()
    
    # Constructing the adjacency(similarity) matrix 
    A = np.zeros((n_nodes, n_nodes))
    pos = {n:i for i,n in enumerate(order)} # map node to position, fix for nodes named as string
    
    for node1, node2 in G.edges:
        A[pos[node1], pos[node2]] = 1
        A[pos[node2], pos[node1]] = 1  
    
    return A


# spectral clustering with the given epsilon, the distance critera for two pooints to be considered in the same cluster
def spectral_clustering(G: nx.Graph, order: list):
    print("Starting...")
    
    # create the similarity matrix
    A = adjacency_matrix(G, order)
    print("A done")
    
    # Compute the sum of weights for each node
    degree_sums = np.sum(A, axis=1)

    # Create the degree matrix as a diagonal matrix
    # D = np.diag(degree_sums)
    # D = np.linalg.pinv(D)**(1/2)
    D = np.diag((1/degree_sums)**(1/2)) # Matrix is positive semi-definite + all edges has a path to each other and therefore has non-zero diagonal, then square-root for normalising
    print("D done")
    # create the normalized Laplacian matrix
    # print(nx.linalg.normalized_laplacian_matrix(G))
    L = np.identity(len(order)) - D @ A @ D
    print("L done")
    del A # free up memory
    del D # free up memory
    # computing the eigenvector for the second-smallest eigenvalue    
    eigval, eigvecs = np.linalg.eig(L) # unpack eigenvalues/-vectors
    idx = eigval.argsort()[1]          # index of second largest eigenvalue
    z_eigvec = eigvecs[:,idx]          # eigenvec w.r.t. second smallest eigenvalue
    
    partition = (z_eigvec >= 0)+0
    
    # add group partition
    for idx,node in enumerate(order):
        G.nodes[node]["group"] = partition[idx]
    
    # save
    full_path = "/work3/s204163/wiki/graph-partitioning/spectral_graph_001"
    with open(f"{full_path}.pkl", "wb") as handle:
        pickle.dump(G, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

    return 


if __name__ == "__main__":
    path = "/work3/s204163/wiki/graph-partitioning/003_37292_subgraph.pkl"
    with open(path, "rb") as f:
        G: nx.Graph = pickle.load(f)
    
    Order = list(G.nodes)
    spectral_clustering(G, Order)
