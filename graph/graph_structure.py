# Default Imports
from dataclasses import dataclass
from tqdm import tqdm # Progress Bar

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

@dataclass
class Article:
    article_id : set[str]
    user_ids : set[str]
    
@dataclass
class User:
    user_id : str
    article_ids : set[str]


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
        
    
    # Set weights between nodes
    # TODO - Given an integer, set the weights of the graph
    def add_edge(self, u, v, weight: int):
        # check if edge exists
        if self.graph.has_edge(u, v):
            # Update weight
            self.graph[u][v]['weight'] += weight
        else:
            self.graph.add_edge(u, v, weight=weight)
        
        

    # TODO - Method for calculating weights between nodes
    def calculate_weights(self, articles: dict[str, Article]):
        for article in articles.values():
            edges = set()
            for user_id in tqdm(article.user_ids):
                for user_id2 in article.user_ids:
                    if user_id != user_id2:
                        if (user_id2, user_id) in edges:
                            continue
                        edges.add((user_id, user_id2))
            
            for edge in edges:
                user_id, user_id2 = edge
                self.add_edge(user_id, user_id2, 1)
                
                

if __name__ == "__main__":
    
    # PATH
    file_path = '/work3/s204163/wiki/wiki-revisions-filtered.bz2'
    
    N = 100000

    # # Create a graph
    G = Revision_User_Graph()
    
    # Get dataframe of revisions
    df_revisions = read_revisions(file_path, N=N)
    df_revisions = df_revisions[['article_id', 'revision_id', 'user_id', 'category']]
    
    # Count the number of unique user_id in df_revisions
    print(len(df_revisions['user_id'].unique()))
    
    
    users = {}
    articles = {}
    
    # For each revision add a node to the graph
    for index, row in df_revisions.iterrows():
        # Create revision object
        revision = Revision(row["article_id"], row["revision_id"], row["user_id"], row["category"])        
        
        # Create user object
        user = User(row["user_id"], {row["article_id"]})
        
        # Create article object
        article = Article(row["article_id"], {row["user_id"]})

        #check if user is in users
        if user.user_id in users:
            # Add article_id to user
            users[user.user_id].article_ids.add(article.article_id)
        else:
            # Add user to users        
            users[user.user_id] = user
            
        #check if article is in articles
        if article.article_id in articles:
            # Add user_id to article
            articles[article.article_id].user_ids.add(user.user_id)
        else:
            # Add article to articles        
            articles[article.article_id] = article
        
        # Add revision to graph
        G.add_revision(revision)
    
    G.calculate_weights(articles)
    
    # loop over all edges in the graph G
    for u, v, weight in tqdm(G.graph.edges.data('weight')):
        if weight > 1:
            print("Edge has weight > 1")            
            print(f"(Edge between: ({u}, {v}) with weight: {weight})")
    
    print("Number of edges in the graph: ", G.graph.number_of_edges())

    
    
    
        

        
        
    
    # G.visualize()