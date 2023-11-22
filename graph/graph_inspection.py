from graph_structure import Revision_User_Graph
import sys


if __name__ == '__main__':
    G = Revision_User_Graph()
    filepath = "/work3/s204163/wiki/graph_logs/graphs/graph-100000-2023-11-14.22:49.pickle"

    G.load_graph(filepath)
    
    print(G.stats(memory_usage=True))