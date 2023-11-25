import glob
import pickle
import numpy as np
import networkx as nx

percent_include = 0.01
path = "/work3/s204163/wiki/graph_logs/graphs/filtered_article_graphs/graph-final.pickle"
with open(path, "rb") as f:
    G: nx.Graph = pickle.load(f)

# Get biggest sub-graph
imax = np.argmax([len(c) for c in nx.connected_components(G)])
Gx: nx.Graph = G.subgraph(list(nx.connected_components(G))[imax])

extension:str = "pkl"
full_path = "/work3/s204163/wiki/test/biggest_subgraph"
with open(f"{full_path}.{extension}", "wb") as handle:
    pickle.dump(Gx, handle, protocol=pickle.HIGHEST_PROTOCOL)


# Get xx% of graph randomly
article_nodes = [node for node in Gx.nodes if Gx.nodes[node]['article']]
n_article = len(article_nodes)
# print(len(article_nodes))
selected = np.random.permutation(range(n_article))[:int(n_article*percent_include)]
n_selected = len(selected)
article_out = [article_nodes[i] for i in selected]
G_sub = set(article_out)
[G_sub.update(set(Gx.neighbors(node))) for node in article_out]
n_sub = len(G_sub)
Gxx = Gx.subgraph(G_sub)
# # Get quantiles
# count = {node:len(Gx.edges(node)) for node in Gx.nodes if Gx.nodes[node]['article']}
# node_list  = np.array(list(count.keys()))
# node_count = np.array(list(count.values()))
# min_val = np.percentile(node_count,45) #>> 15
# max_val = np.percentile(node_count,55) #>> 25
# arr_qua = node_list[(node_count >= min_val) & (node_count <= max_val)]
# Gsub = set(arr_qua)
# [Gsub.update(set(Gx.neighbors(node))) for node in arr_qua]
# print(len(arr_qua),len(count)) #>> 1935 16845
# print(len(Gsub)) #>> 37448
print(n_article,n_selected,(n_sub-n_selected)/n_selected)

# extension:str = "pkl"
# full_path = "/work3/s204163/wiki/test/subgraph_"+str(percent_include)
# with open(f"{full_path}.{extension}", "wb") as handle:
#     pickle.dump(Gxx, handle, protocol=pickle.HIGHEST_PROTOCOL)