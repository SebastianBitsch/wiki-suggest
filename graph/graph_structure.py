import sys
import os

import networkx as nx
import netwulf as nw

from read_data import read_revisions

from dataclasses import dataclass


@dataclass
class Revision:
    revision_id : str
    user_id : str
    article_id : set[str]
    category : set[str]

# Create a graph
class Revision_User_Graph:
    def __init__(self):
        self.graph = nx.Graph()

    
    def add_revision(self, revision: Revision):
        self.graph.add_node(revision.user_id)


if __name__ == "__main__":
    print("Hello World")
    
    # PATH
    file_path = '/work3/s204163/wiki/wiki-revisions-dataset.bz2'
    os.path.exists(file_path)

    # # Create a graph
    G = nx.Graph()
    read_revisions(file_path, N=10)