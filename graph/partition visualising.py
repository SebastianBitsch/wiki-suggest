import pickle
import numpy as np
import networkx as nx
import netwulf as nw
import matplotlib.pyplot as plt

# G = nx.path_graph(4)
# shells = [[0], [1, 2, 3]]
# pos = nx.shell_layout(G, shells)
# raise Exception()

path = "/work3/s204163/wiki/graph-partitioning/GirvanNewmanGraph_final_0.pkl"
with open(path, "rb") as f:
    G: nx.Graph = pickle.load(f)

for idx,com in enumerate(nx.connected_components(G)):
    print(len(com))
    for node in com:
        G.nodes[node]["group_idx"] = idx
with open("/work3/s204163/wiki/graph-partitioning/GirvanNewmanGraph_partitions_1.pkl", "wb") as handle:
    pickle.dump(G, handle, protocol=pickle.HIGHEST_PROTOCOL)

coloring  = {
    (0,True ): '#4805d7',
    (0,False): '#4805d7',
    (1,True ): '#07d77c',
    (1,False): '#07d77c'
             }
gget = lambda node,info: G.nodes[node][info]
color_map = [coloring[(gget(node,"group"),gget(node,"article"))] for node in G.nodes]
legends   = [gget(node,"group") for node in G.nodes]

G0 = [node for node in G.nodes if G.nodes[node]["group"] == 0]
G1 = [node for node in G.nodes if G.nodes[node]["group"] == 1]
Gu = [node for node in G.nodes if not G.nodes[node]["article"]]
Ga = [node for node in G.nodes if     G.nodes[node]["article"]]
# print(sum(1 for _ in nx.connected_components(G1)))
# print(sum(1 for _ in nx.connected_components(G2)))

def nx_plot(G, pos=nx.random_layout(G), name="default"):
    plt.clf()
    nx.draw(G, node_size=2, node_color=color_map, pos=pos)
    # plt.legend()
    plt.savefig("G_001_"+name+".png")

# nx_plot(G)
# nx_plot(G, nx.bipartite_layout(G,Gu), "bipartite")
# nx_plot(G, nx.circular_layout(G), "circular")
nx_plot(G, nx.kamada_kawai_layout(G, weight=None), "kamada_kawai")
# nx_plot(G, nx.planar_layout(G), "planar")
# nx_plot(G, nx.shell_layout(G,[G0,G1]), "shell")
# nx_plot(G, nx.spring_layout(G), "spr-ing")
# nx_plot(G, nx.spiral_layout(G), "spi-ral")
# nx_plot(G, nx.multipartite_layout(G, subset_key="group"), "multipartite")


# fig, ax = plt.subplots(nrows=1, ncols=1)
# fig.set_facecolor("black")
# plt.savefig("G_samp_black.png")
