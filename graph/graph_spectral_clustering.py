import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering
from sklearn import metrics
import pickle

# Get your mentioned graph
# np.random.seed(1)
# G = nx.karate_club_graph()

path = "/work3/s204163/wiki/logs/graph.adjlist-2023-11-13 11:01:27.497461"
with open(path, "rb") as f:
    G : nx.Graph = pickle.load(f)

# Get ground-truth: club-labels -> transform to 0/1 np-array
# (possible overcomplicated networkx usage here)
gt_dict = nx.get_node_attributes(G, 'club')
# gt = [gt_dict[i] for i in G.nodes()]
# gt = np.array([0 if i == 'Mr. Hi' else 1 for i in gt])
gt = np.array([int(gt_dict[i] != 'Mr. Hi') for i in G.nodes()]) # Single looping


# Get adjacency-matrix as numpy-array
adj_mat = nx.to_numpy_array(G)

# Cluster
sc = SpectralClustering(2, affinity='precomputed', n_init=100)
sc.fit(adj_mat)


# Compare ground-truth and clustering-results
print('                      Ground truth', gt)
print('               Spectral clustering', sc.labels_)
print('  -inverted spectral (permutation)', 1 - sc.labels_)
print(' Agreement between ground/spectral', (gt == sc.labels_)+0) # add 0 to get 0/1


# Calculate some clustering metrics
print(metrics.adjusted_rand_score(gt, sc.labels_))
print(metrics.adjusted_mutual_info_score(gt, sc.labels_))

# Spectral clustering mixed with k_means
sc_k_means = SpectralClustering(2, affinity='precomputed', n_init=100, assign_labels='kmeans')

sc_other = SpectralClustering(2, affinity='precomputed', n_init=100, assign_labels='descritized')