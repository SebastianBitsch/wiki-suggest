import networkx as nx
import matplotlib.pyplot as plt
import pickle
import random
from tqdm import tqdm
import glob
# from utils.pickle_dump import pickle_dump


# counts number of shortest path to node from root, part 1+2 of betweenness
def path_weighting(G: nx.Graph, n_random_nodes: int = -1):
    node_weighting = {}
    n_random_nodes = min(n_random_nodes, G.number_of_nodes()) if n_random_nodes > 0 else G.number_of_nodes()
    # print(n_random_nodes)
    for root in tqdm(random.sample(G.nodes, n_random_nodes), mininterval=int(n_random_nodes*0.1)): # Foreach node as root
        queue        = [root]
        node_paths   = {root:[None]}
        dist_node    = {0:[root]}
        visited_dist = {root:0} # visted node: distance from root
        for nodeP in queue: # Run bfs
            for nodeC in set(G.neighbors(nodeP)): # Neighbours/Childrens
                DistRoot = visited_dist[nodeP] + G.edges[nodeP,nodeC].get('weight',1) # distance from root
                is_visited = nodeC in visited_dist
                if   is_visited and DistRoot >  visited_dist[nodeC]: continue
                elif is_visited and DistRoot == visited_dist[nodeC]:
                    node_paths[nodeC].append(nodeP)
                elif is_visited:#   DistRoot <  visited_dist[nodeC]
                    node_paths[nodeC]  = [nodeP]
                    dist_node[visited_dist[nodeC]].remove(nodeC)
                else:
                    node_paths[nodeC]  = [nodeP]
                dist_node[DistRoot] = [*dist_node.get(DistRoot,[]), nodeC]
                queue.append(nodeC)
                visited_dist[nodeC] = DistRoot
        dist_node = {key:val for key,val in dist_node.items() if val} # remove empties
        node_weighting[root] = (node_paths,dist_node)
    return node_weighting
        
def bc_wedges(G: nx.Graph, ddist: dict): # betweenness centrality for edges w. weights
    minmax = lambda pair: (min(*pair),max(*pair))
    betweennees = {minmax(n_pair):0 for n_pair in G.edges()}
    # print(betweennees)
    for root,dist_dict in ddist.items():
        # print("Root:",root)
        node_paths = dist_dict[0]
        dist_node  = dist_dict[1]
        Order = sorted(dist_node,reverse=True)
        prev_br = {}
        for idxD in range(len(Order)-1):
            # print(node_paths)
            # print(dist_node)
            # raise Exception()
            for n_from in set(dist_node[Order[idxD]]):
                for n_to in node_paths[n_from]:
                    # print(n_from,n_to)
                    # if minmax([n_from,n_to]) in betweennees:
                    if n_to == None:
                        continue
                    l2_udv = len(node_paths[n_to])/len(node_paths[n_from])
                    
                    br_uv = l2_udv + l2_udv*prev_br.get(n_from,0)
                    betweennees[minmax([n_from,n_to])] += br_uv
                    prev_br[n_to] = prev_br.get(n_to, 0) + br_uv
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
    filepath:str = "/work3/s204163/wiki/"
    extension:str = "pkl"
    
    # output_path = "/work3/s204163/wiki/test/"
    # Load karate graph and find communities using Girvan-Newman
    # G = nx.karate_club_graph()

    path = "/work3/s204163/wiki/test/biggest_subgraph.pkl"
    with open(path, "rb") as f:
        G: nx.Graph = pickle.load(f)
    
    dict_path = path_weighting(G, 1)
    bc_dict = bc_wedges(G, dict_path)
    # pickle_dump(bc_dict,"test/betweenness")
    
    full_path = filepath + "test/betweenness"
    n_exist = len(glob.glob(full_path+"*"))
    with open(f"{full_path}_{n_exist}.{extension}") as handle:
        pickle.dump(bc_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    GN_out = Girvan_Newman(G,bc_dict,10)
    full_path = filepath + "test/GirvinNewman"
    n_exist = len(glob.glob(full_path+"*"))
    with open(f"{full_path}_{n_exist}.{extension}") as handle:
        pickle.dump(GN_out, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # pickle_dump(GN_out,"test/GirvinNewman")
