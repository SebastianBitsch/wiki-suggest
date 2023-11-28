import networkx as nx
import pickle
import random
from tqdm import tqdm
import glob


# counts number of shortest path to node from root, part 1+2 of betweenness, all edge weights are 1
def path_counting(G: nx.Graph, n_random_betweenness: int|float = -1):
    dict_list = {}
    # decide number of nodes 
    if type(n_random_betweenness) == int:
        n_random_betweenness = min(n_random_betweenness, G.number_of_nodes()) if n_random_betweenness > 0 else G.number_of_nodes()
    else:
        assert (n_random_betweenness <= 1) & (n_random_betweenness >= 0), "For floats, between 0 and 1"
        n_random_betweenness = int(G.number_of_nodes()*n_random_betweenness)
    # Foreach node as root
    for root in random.sample(G.nodes, n_random_betweenness): 
        dist_dict = {0: {root: 1}}
        queue     = set((root,))
        visited   = set((root,))
        dist = 1
        while True: # Run bfs
            next_queue = []
            for node in queue: # Neighbours
                next_queue.extend(list(G.neighbors(node))*dist_dict[dist-1][node]) # memory inefficient
            unique_nv = set(next_queue) - visited # Get individual which are yet visited
            # if no new neighbour
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
def betweenness_edges(G: nx.Graph, ddist: dict): 
    minmax = lambda x,y: (min(x,y),max(x,y))
    betweennees = {minmax(*n_pair):0 for n_pair in G.edges()}
    for root,dist in ddist.items():
        prev_br = {}
        for idx in reversed(range(max(dist))):
            for n_to in dist[idx]: #                    ┌─> to node
                for n_from in dist[idx+1]: # from node ─┘
                    if minmax(n_from,n_to) in betweennees: # edge exist
                        l2_udv = dist[idx][n_to]/dist[idx+1][n_from] # computing betweenness for edge
                        br_uv = l2_udv + l2_udv*prev_br.get((idx+1,n_from),0)
                        betweennees[minmax(n_from,n_to)] += br_uv
                        prev_br[(idx,n_to)] = prev_br.get((idx,n_to), 0) + br_uv
    for key,val in list(betweennees.items()):
        betweennees[key] = val/2 # shortest paths counted twice, remove half
    return betweennees

def girvan_newman_cut(g: nx.Graph, betweenness: dict):
    # find the edge with largest betweenness
    n_subgraphs = sum(1 for _ in nx.connected_components(g))
    g.remove_edge(*max(betweenness, key=betweenness.get))
    new_subgraph_formed = n_subgraphs != sum(1 for _ in nx.connected_components(g))
    return g, new_subgraph_formed
    
def run_girvan_newman(G: nx.Graph, n_random_betweenness: int|float = -1, k_cuts: int = -1, k_subs: int = -1):
    """ 
    Run Girvan Newman on Graph G 

    Args:
        G (nx.Graph): networkx graph
        n_random_betweenness (int | float, optional): number of nodes used to calculate betweenness. Defaults to -1.
        k_cuts (int, optional): number of cuts. Defaults to -1.
        k_subs (int, optional): number of subgraphs. Defaults to -1.

    Returns:
        nx.Graph: returns G with cuts
    """
    g = G.copy()
    if k_subs > 0: # for number of subs
        count = 1
        while count != k_subs:
            dict_path   = path_counting(g, n_random_betweenness)
            bc_dict     = betweenness_edges(g, dict_path)
            g, NSF      = girvan_newman_cut(g,bc_dict)
            if NSF: # new subgroup formed
                print(f"{count}/{k_subs}") # progress
                count += 1
                full_path = filepath + "graph-partitioning/GirvanNewmanGraph_subs"+str(count)
                n_exist = len(glob.glob(full_path+"*"))
                with open(f"{full_path}_{n_exist}.{extension}", "wb") as handle:
                    pickle.dump(g, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else: # for number of cuts
        for idx in range(max(k_cuts,1)): # runs minimum once
            # print(True)
            dict_path   = path_counting(g, n_random_betweenness)
            bc_dict     = betweenness_edges(g, dict_path)
            g,_         = girvan_newman_cut(g,bc_dict)
            
            full_path = filepath + "graph-partitioning/GirvanNewmanGraph_i"+str(idx)
            n_exist = len(glob.glob(full_path+"*"))
            with open(f"{full_path}_{n_exist}.{extension}", "wb") as handle:
                pickle.dump(g, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return g

if __name__ == "__main__":
    filepath:str = "/work3/s204163/wiki/"
    extension:str = "pkl"
    
    path = "/work3/s204163/wiki/graph-partitioning/001_8750_subgraph.pkl"
    with open(path, "rb") as f:
        G: nx.Graph = pickle.load(f)
    G = run_girvan_newman(G,n_random_betweenness=20,k_subs=13)
    
    full_path = filepath + "graph-partitioning/GirvanNewmanGraph_final"
    n_exist = len(glob.glob(full_path+"*"))
    with open(f"{full_path}_{n_exist}.{extension}", "wb") as handle:
        pickle.dump(G, handle, protocol=pickle.HIGHEST_PROTOCOL)
    