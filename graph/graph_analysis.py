import networkx as nx


# TODO : Add a function that given a graph, returns the modularity of the graph
def modularity(G : nx.Graph, partition : list[list[str]]):
    # get the number of edges in the graph
    m = G.number_of_edges()

    # create a dictionary that maps each node to its community
    communities = {}
    for i, nodes in enumerate(partition):
        for node in nodes:
            communities[node] = i

    # calculate the modularity
    Q = 0
    for i, nodes1 in enumerate(partition):
        for j, nodes2 in enumerate(partition):
            if i == j:
                # calculate the fraction of edges within the community
                lc = sum(list(dict(G.subgraph(nodes1).degree()).values())) / (2.0 * m)
                Q += (lc - np.square(lc))
            else:
                # calculate the fraction of edges between communities
                lnc = sum(G.subgraph(nodes1).degree(nbunch=nodes2)) / (2.0 * m)
                Q += lnc

    return Q

def partitioning(G : nx.Graph) -> list[list[str]]:
    # TODO : Implement the partitioning algorithm
    # TODO : Return a list of lists, where each list is a community
    # TODO : The partitioning algorithm should be based on the Girvan-Newman algorithm
    # TODO : The algorithm should stop when the modularity of the graph is maximized
    # TODO : The algorithm sh
    raise NotImplementedError("Not implemented yet")