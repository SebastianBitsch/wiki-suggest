import networkx as nx
import matplotlib.pyplot as plt
import pickle
import glob
import random
from tqdm import tqdm



# counts number of shortest path to node from root, part 1+2 of betweenness
def path_counting(G: nx.Graph, n_random_nodes: int = -1):
    dict_list = {}
    n_random_nodes = min(n_random_nodes, G.number_of_nodes()) if n_random_nodes > 0 else G.number_of_nodes()
    for root in tqdm(random.sample(G.nodes, n_random_nodes), mininterval=int(n_random_nodes*0.1)): # Foreach node as root
        dist_dict = {0: {root: 1}}
        queue     = set((root,))
        visited   = set((root,))
        dist = 1
        while True: # Run bfs
            
            
            next_queue = {}
            for node in queue: 
                for nodeb in set(G.neighbors(node))-unique_nv: # Neighbours
                    next_queue[nodeb] = next_queue.get() #G.edges[node,nodeb]['weight']
                # next_queue.extend(list(G.neighbors(node))*dist_dict[dist-1][node]) # memory inefficient
            unique_nv = set(next_queue) - visited # Get individual which are yet visited
            # Check if no neighbour
            if not unique_nv: break
            # 
            step_dict = {}
            for n in unique_nv:
                step_dict[n] = next_queue.count(n)

            
            dist_dict[dist] = step_dict
            visited.update(unique_nv)
            queue = unique_nv
            dist += 1
        dict_list[root] = dist_dict
    return dict_list

# betweenness centrality for edges
def bc_edges(G: nx.Graph, ddist: dict): 
    minmax = lambda x,y: (min(x,y),max(x,y))
    betweennees = {minmax(*n_pair):0 for n_pair in G.edges()}
    for root,dist in tqdm(ddist.items(), mininterval=int(len(ddist)*0.1)):
        prev_br = {}
        for idx in reversed(range(max(dist))):
            for n_to in dist[idx]: #                      __\  to node
                for n_from in dist[idx+1]: # from node __/  /
                    if minmax(n_from,n_to) in betweennees: # has an edge
                        l2_udv = dist[idx][n_to]/dist[idx+1][n_from]
                        br_uv = l2_udv + l2_udv*prev_br.get((idx+1,n_from),0)
                        betweennees[minmax(n_from,n_to)] += br_uv
                        prev_br[(idx,n_to)] = prev_br.get((idx,n_to), 0) + br_uv
    for key,val in list(betweennees.items()):
        betweennees[key] = val/2
    return betweennees


def Girvan_Newman(g: nx.Graph, betweenness: dict, k: int = 1, remove_singles = True):
    # g = G.copy() # Remove after
    ordered_betwns = sorted(betweenness, key=betweenness.get, reverse=True)
    n_subg = 2
    for edge in ordered_betwns:
        g.remove_edge(*edge)
        if edge[0] not in nx.connected.node_connected_component(g,edge[1]):
            if remove_singles and (len(nx.connected.node_connected_component(g,edge[0])) == 1 or len(nx.connected.node_connected_component(g,edge[1])) == 1):
                continue
            if n_subg-1 == k:
                if remove_singles:
                    return [subgraph for subgraph in nx.connected_components(g) if len(subgraph) != 1]
                return list(nx.connected_components(g)), True
            n_subg += 1
        else:
            g.add_edge(*edge)
    return list(nx.connected_components(g)), False

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

if __name__ == "__main__":
    output_path = "/work3/s204163/wiki/test/"
    # Load karate graph and find communities using Girvan-Newman
    # G = nx.karate_club_graph()

    path = "/work3/s204163/wiki/logs/graph.adjlist-2023-11-13 11:01:27.497461"
    with open(path, "rb") as f:
        G: nx.Graph = pickle.load(f)
    
    dict_path = path_counting(G, -1)
    bc_dict = bc_edges(G, dict_path)
    pickle.dump(bc_dict, output_path+"betweenness.pkl")
    GN_out = Girvan_Newman(G,bc_dict,10)
    pickle.dump(GN_out, output_path+"GirvinNewman.pkl")

