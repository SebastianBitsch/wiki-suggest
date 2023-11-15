import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import glob

output_path = "/work3/s204163/wiki/test/"
# Load karate graph and find communities using Girvan-Newman
# G = nx.karate_club_graph()

path = "/work3/s204163/wiki/logs/graph.adjlist-2023-11-13 11:01:27.497461"
with open(path, "rb") as f:
    G : nx.Graph = pickle.load(f)

# print(G.number_of_edges(), G.number_of_nodes())
# raise Exception() 

communities = list(nx.community.girvan_newman(G))
output_increment = len(glob.glob(output_path + "communities_*.pkl"))
with open(f"{output_path}communities_{output_increment}.pkl", "bx") as f:
    pickle.dump(communities, f)

# Modularity -> measures the strength of division of a network into modules
modularity_df = pd.DataFrame(
    [
        [k + 1, nx.community.modularity(G, communities[k])]
        for k in range(len(communities))
    ],
    columns=["k", "modularity"],    
)

print(modularity_df)

# function to create node colour list
def create_community_node_colors(graph, communities):
    number_of_colors = len(communities[0])
    colors = ["#D4FCB1", "#CDC5FC", "#FFC2C4", "#F2D140", "#BCC6C8"][:number_of_colors]
    node_colors = []
    for node in graph:
        current_community_index = 0
        for community in communities:
            if node in community:
                node_colors.append(colors[current_community_index])
                break
            current_community_index += 1
    return node_colors


# function to plot graph with node colouring based on communities
def visualize_communities(graph, communities, i):
    node_colors = create_community_node_colors(graph, communities)
    modularity = round(nx.community.modularity(graph, communities), 6)
    title = f"Community Visualization of {len(communities)} Communities with modularity of {modularity}"
    pos = nx.spring_layout(graph, k=0.3, iterations=50, seed=2)
    plt.subplot(3, 1, i)
    plt.title(title)
    nx.draw(
        graph,
        pos=pos,
        node_size=1000,
        node_color=node_colors,
        with_labels=True,
        font_size=20,
        font_color="black",
    )


fig, ax = plt.subplots(3, figsize=(15, 20))

# Plot graph with colouring based on communities
visualize_communities(G, communities[0], 1)
visualize_communities(G, communities[3], 2)

# Plot change in modularity as the important edges are removed
modularity_df.plot.bar(
    x="k",
    ax=ax[2],
    color="#F2D140",
    title="Modularity Trend for Girvan-Newman Community Detection",
)
# plt.show()
plt.savefig(output_path+"modularity_df.png")


# Betweenness centrality
def betweenness_centrality(G : nx.Graph) -> dict:
    return betweenness_centrality(G)


#def partitioning(G : nx.Graph) -> list[set[str]]:
#    return nx.community.louvain_communities(G, seed=123)
#    # TODO : Implement the partitioning algorithm
#    # TODO : Return a list of lists, where each list is a community
#    # TODO : The partitioning algorithm should be based on the Girvan-Newman algorithm
#    # TODO : The algorithm should stop when the modularity of the graph is maximized
#    # TODO : The algorithm sh
#
## TODO : Add a function that given a graph, returns the modularity of the graph
#def modularity(G : nx.Graph, partition : list[set[str]]):
#    return nx.community.modularity(G, partition)
#    '''
#    # get the number of edges in the graph
#    m = G.number_of_edges()
#
#    # create a dictionary that maps each node to its community
#    communities = {}
#    for i, nodes in enumerate(partition):
#        for node in nodes:
#            communities[node] = i
#
#    # calculate the modularity
#    Q = 0
#    for i, nodes1 in enumerate(partition):
#        for j, nodes2 in enumerate(partition):
#            if i == j:
#                # calculate the fraction of edges within the community
#                lc = sum(list(dict(G.subgraph(nodes1).degree()).values())) / (2.0 * m)
#                Q += (lc - np.square(lc))
#            else:
#                # calculate the fraction of edges between communities
#                lnc = sum(G.subgraph(nodes1).degree(nbunch=nodes2)) / (2.0 * m)
#                Q += lnc
#
#    return Q
#    '''
