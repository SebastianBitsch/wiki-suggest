import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering
from sklearn import metrics
np.random.seed(1)

# Get your mentioned graph
G = nx.karate_club_graph()

# Get ground-truth: club-labels -> transform to 0/1 np-array
# (possible overcomplicated networkx usage here)
gt_dict = nx.get_node_attributes(G, 'club')
gt = [gt_dict[i] for i in G.nodes()]
gt = np.array([0 if i == 'Mr. Hi' else 1 for i in gt])

# Get adjacency-matrix as numpy-array
adj_mat = nx.to_numpy_array(G)

print('ground truth')
print(gt)

# Cluster
sc = SpectralClustering(2, affinity='precomputed', n_init=100)
sc.fit(adjmat)

# Compare ground-truth and clustering-results
print('spectral clustering')
print(sc.labels)
print('just for better-visualization: invert clusters (permutation)')
print(np.abs(sc.labels_ - 1))

# Calculate some clustering metrics
print(metrics.adjusted_randscore(gt, sc.labels))
print(metrics.adjusted_mutual_infoscore(gt, sc.labels))

# Spectral clustering mixed with k_means
sc_k_means = SpectralClustering(2, affinity='precomputed', n_init=100, assign_labels='kmeans')

sc_other = SpectralClustering(2, affinity='precomputed', n_init=100, assign_labels='descritized')