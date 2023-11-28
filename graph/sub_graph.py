import glob
import pickle
import numpy as np
import networkx as nx
import netwulf
import matplotlib.pyplot as plt

def save_graph(G: nx.Graph, filename = "Test"):
    print([len(c) for c in nx.connected_components(G)])
    full_path = "/work3/s204163/wiki/graph-partitioning/"+filename
    with open(f"{full_path}.pkl", "wb") as handle:
        pickle.dump(G, handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_biggest_sub_graph(G: nx.Graph):
    imax = np.argmax([len(c) for c in nx.connected_components(G)])
    Gx: nx.Graph = G.subgraph(list(nx.connected_components(G))[imax])
    return Gx

def sample_xxP_of_graph(G: nx.Graph, percent_include = 0.01):
    article_nodes = [node for node in G.nodes if G.nodes[node]['article']]
    n_article = len(article_nodes)
    # print(len(article_nodes))
    selected = np.random.permutation(range(n_article))[:int(n_article*percent_include)]
    n_selected = len(selected)
    article_out = [article_nodes[i] for i in selected]
    G_sub = set(article_out)
    [G_sub.update(set(G.neighbors(node))) for node in article_out]
    n_sub = len(G_sub)
    Gx = G.subgraph(G_sub)
    # Get quantiles
    # count = {node:len(G.edges(node)) for node in G.nodes if G.nodes[node]['article']}
    # node_list  = np.array(list(count.keys()))
    # node_count = np.array(list(count.values()))
    # min_val = np.percentile(node_count,45) #>> 15
    # max_val = np.percentile(node_count,55) #>> 25
    # arr_qua = node_list[(node_count >= min_val) & (node_count <= max_val)]
    # Gsub = set(arr_qua)
    # [Gsub.update(set(G.neighbors(node))) for node in arr_qua]
    # print(len(arr_qua),len(count)) #>> 1935 16845
    # print(len(Gsub)) #>> 37448
    # print(n_article,n_selected,(n_sub-n_selected)/n_selected)

    # extension:str = "pkl"
    # full_path = "/work3/s204163/wiki/graph-partitioning/subgraph_"+str(percent_include)
    # with open(f"{full_path}.{extension}", "wb") as handle:
    #     pickle.dump(Gxx, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # print(sorted([len(c) for c in nx.connected_components(Gxx)]))
    return Gx

def trim_single_users(G: nx.Graph):
    G = G.copy()
    user_nodes = {node for node in G.nodes if not G.nodes[node]['article']}
    for n_user in user_nodes:
        nb_gen = G.neighbors(n_user)
        if sum(1 for _ in nb_gen) == 1: # memory efficient length of generator
            nb = next(G.neighbors(n_user))
            G.nodes[nb]["single_users"] = 1 + G.nodes[nb].get("single_users", 0)
            G.remove_node(n_user)
    with open("/work3/s204163/wiki/graph-partitioning/TSU_graph.pkl", "wb") as handle:
        pickle.dump(G, handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_xxP_biggest_subgraph(G: nx.Graph, p_include = 0.01):
    Gx  = sample_xxP_of_graph(G, p_include)
    Gxx = get_biggest_sub_graph(Gx) 
    save_graph(Gxx, str(int(p_include*100)).rjust(3,"0")+"_largest_subgraph")

# path = "/work3/s204163/wiki/graph-partitioning/biggest_subgraph.pkl"
path = "/work3/s204163/wiki/graph-partitioning/003_37292_subgraph.pkl"
# G.number_of_nodes()   >> 37292
# len(list_val)         >>  3809
# list_val.count(1)     >>  3787
with open(path, "rb") as f:
    G: nx.Graph = pickle.load(f)

# print(len(G.nodes))
get_xxP_biggest_subgraph(G, 0.01)

raise Exception()