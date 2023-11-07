# Default Imports
from dataclasses import dataclass

# Graph Imports
import networkx as nx # Graph Structure
import netwulf as nw # Visualize Graph

# Custom Imports
from utils.read_data import read_revisions



# Revision class, for sending information around as an object
@dataclass
class Revision:
    article_id : set[str]
    revision_id : str
    user_id : str
    category : set[str]


class Revision_User_Graph:
    def __init__(self):
        self.graph = nx.Graph()

    # Adds a single node to the graph from user_id
    def add_revision(self, revision: Revision):
        # If the user_id is already in the graph, it is not added.
        self.graph.add_node(revision.user_id)
        
    # Opens a local server for viewing the graph
    def visualize(self):
        nw.visualize(self.graph)


if __name__ == "__main__":
    print("Hello World")
    
    # PATH
    file_path = '/work3/s204163/wiki/wiki-revisions-dataset.bz2'

    # # Create a graph
    G = Revision_User_Graph()
    
    # Get dataframe of revisions
    df_revisions = read_revisions(file_path, N=10)
    df_revisions = df_revisions[['article_id', 'revision_id', 'user_id', 'category']]
    
    # Count the number of unique user_id in df_revisions
    print(len(df_revisions['user_id'].unique()))
    
    # For each revision add a node to the graph
    for index, row in df_revisions.iterrows():
        revision = Revision(row["article_id"], row["revision_id"], row["user_id"], row["category"])        
        G.add_revision(revision)
    
    G.visualize()