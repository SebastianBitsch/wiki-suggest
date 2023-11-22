# Default Imports
from dataclasses import dataclass, field
from tqdm import tqdm # Progress Bar
import sys
import pickle
from datetime import datetime
import os

# Graph Imports
import networkx as nx # Graph Structure
import netwulf as nw # Visualize Graph

# Custom Imports
from utils.read_data import read_revisions
from batchjob_utils import log_message, memory_usage_of

# Revision class, for sending information around as an object
@dataclass
class Revision:
    article_id : set[str]
    revision_id : str
    user_id : str
    category : set[str]

@dataclass
class Article:
    article_id : str
    user_ids : set[str] = field(default_factory=set)
    
@dataclass
class User:
    user_id : str
    article_ids : set[str] = field(default_factory=set)


class Revision_User_Graph:
    def __init__(self):
        self.graph = nx.Graph()
        self.tqdm_disable = True
    
    def __repr__(self):
        return f"Revision_User_Graph(graph={self.graph})"
    
    def stats(self, memory_usage : bool = False):
        stats = [
            f"Graph stats:",
            f"Number of nodes: {self.graph.number_of_nodes()}",
            f"Number of edges: {self.graph.number_of_edges()}",
            f"max degree: {max(dict(self.graph.degree()).values())}",
            f"valid weights: {sum([1 for u, v, weight in self.graph.edges.data('weight') if weight > 1])}",
            ]
        
        if memory_usage:
            mem_nodes, mem_nodes_message = memory_usage_of(list(self.graph.nodes()), "Graph nodes")
            mem_edges, mem_edges_message = memory_usage_of(list(self.graph.edges()), "Graph edges")
            _, total_mem_message = memory_usage_of(mem_nodes + mem_edges, "Graph nodes and edges")
            
            stats.extend([
                f'\nMemory usage:',
                mem_nodes_message,
                mem_edges_message,
                total_mem_message,
                ])
        
        return "\n".join(stats)
    
    def save_graph(self, file_path: str):
        with open(file_path, "wb") as file: 
            pickle.dump(self.graph, file)
        
    def load_graph(self, file_path: str):
        with open(file_path, "rb") as file: 
            self.graph = pickle.load(file)

    # Adds a single node to the graph from user_id
    def add_revision(self, revision: Revision = None, user_id: str = None):
        # If the user_id is already in the graph, it is not added.
        if user_id:
            self.graph.add_node(user_id)
        if revision:
            self.graph.add_node(revision.user_id)
        return None
        
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
    def calculate_weights(self, articles: list[Article] | dict[str, Article]):
        if isinstance(articles, dict):
            articles = list(articles.values())
        for article in tqdm(articles, disable = self.tqdm_disable):
            edges = set()
            for user_id in article.user_ids:
                for user_id2 in article.user_ids:
                    if user_id != user_id2:
                        if (user_id2, user_id) in edges:
                            continue
                        edges.add((user_id, user_id2))
            
            for edge in edges:
                user_id, user_id2 = edge
                self.add_edge(user_id, user_id2, 1)

    def add_node(self, node:str, article:bool):
        self.graph.add_node(node, article=article)
        
    def add_article(self, article: Article):
        
        self.add_node(article.article_id, article=True)
        
        for user_id in article.user_ids:
            user_id = user_id.strip()
            self.add_node(user_id, article=False)
            self.graph.add_edge(user_id, article.article_id, weight=1)
        
    def create_graph_from_articles(self, articles: list[Article]):
        for article in tqdm(articles, disable = self.tqdm_disable):
            self.add_article(article)
    


def create_graph(file_path, output_file, N, **kwargs) -> nx.Graph:
    # kwargs
    # log_file : str = None, 
    # log_interval : int = None, 
    # tqdm_disable : bool = True
    log_interval = kwargs.get("log_interval", None)
    tqdm_disable = kwargs.get("tqdm_disable", True)
    log_file = kwargs.get("log_file", None)
    console_log = kwargs.get("console_log", False)
    
    
    def log_interval_logic(index):
        if not log_interval:
            return False
        if index % log_interval == 0:
            return True
    
    
    
    # Init Graph and article infrastructure
    G = Revision_User_Graph()
    articles = {}
    
    # Get dataframe of revisions
    df_revisions = read_revisions(file_path, N=N)
    
    # Get only relevant columns
    df_revisions = df_revisions[['article_id', 'user_id']]
    
    # For each revision add a node to the graph
    for index, revision in tqdm(df_revisions.iterrows(), total=len(df_revisions), disable=tqdm_disable):
        if log_interval_logic(index):
            message = f"\nLog #{index//log_interval} for index {index} out of {len(df_revisions)}"
            log_message(message, log_file, console_log=console_log)
                
        # Get data from row
        user_id = revision["user_id"]
        article_id = revision["article_id"]
        
        #Add user_id to article
        article = articles[article_id] = articles.get(article_id, Article(article_id))
        article.user_ids.add(user_id)

        # Add revision to graph
        G.add_revision(user_id = user_id)
        
        if log_interval_logic(index):
            log_message(G.stats(), log_file, console_log=console_log)

    # Create edges between nodes
    G.calculate_weights(articles)
    
    # Print stats
    log_message(G.stats(memory_usage=True), log_file, console_log=console_log)
    log_message(memory_usage_of(articles, "Articles"), log_file, console_log=console_log)
    
    # Save graph
    with open(output_file, "wb") as file: 
        pickle.dump(G.graph, file)
    

    
    # G.visualize()