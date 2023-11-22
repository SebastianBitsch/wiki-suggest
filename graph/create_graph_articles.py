from graph_structure import Revision_User_Graph, Article, User
from batchjob_utils import log_message, memory_usage_of
from datetime import datetime
import os
import pickle
import numpy as np
from tqdm import tqdm
import time
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()

BATCH_SIZE = 1000
TQDM_DISABLE = True
CONSOLE_LOG = True
FORMAT_DATE = datetime.now().strftime('%Y-%m-%d.%H:%M')
START_TIME = time.time()

ARTICLE_PATH = "/work3/s204163/wiki/data-batches/articles_keep_cutoff98_sync.pickle"

OUTPUT_DIR = "/work3/s204163/wiki/graph_logs/graphs/filtered_article_graphs"
LOG_FILENAME = f"/work3/s204163/wiki/graph_logs/logs/FArticleGraph-{FORMAT_DATE}.txt"


def get_batches(data:list, batch_size):
    N = len(data)
    batches = []
    for i in range(0, N, batch_size):
        batches.append(data[i:i+batch_size])
    return batches

def plot_iteration_times(iteration_times):
    plt.figure(figsize=(15, 15))

    plt.plot(iteration_times)
    plt.xlabel("Iteration")
    plt.ylabel("Time (s)")
    plt.title("Time per iteration")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"iteration_times.png"))

def plot_nodes_per_iteration(nodes_per_iteration):
    plt.figure(figsize=(15, 15))
    plt.plot(nodes_per_iteration)
    plt.xlabel("Iteration")
    plt.ylabel("Nodes")
    plt.title("Nodes per iteration")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"nodes_per_iteration.png"))

def plot_edges_per_iteration(edges_per_iteration):
    plt.figure(figsize=(15, 15))

    plt.plot(edges_per_iteration)
    plt.xlabel("Iteration")
    plt.ylabel("Edges")
    plt.title("Edges per iteration")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"edges_per_iteration.png"))

def run():

    # Load data
    with open(ARTICLE_PATH, "rb") as f:
        all_articles = pickle.load(f)
    
    # Init graph
    G = Revision_User_Graph()
    
            
    # Get batches
    batches = get_batches(list(all_articles.values()), BATCH_SIZE)
    
    N_batches = len(batches)

    iteration_times = []
    iteration_nodes = []
    iteration_edges = []
    
    for index, batch in tqdm(enumerate(batches), total = N_batches, disable=TQDM_DISABLE):
        iteration_start = time.time()
        log_message(f"\nBatch #{index} out of {N_batches}", LOG_FILENAME, console_log=CONSOLE_LOG)
        
        # Add articles to graph
        G.create_graph_from_articles(batch)
        
        log_message(G.stats(memory_usage=True), LOG_FILENAME, console_log=CONSOLE_LOG)
        log_message(memory_usage_of(G, "Graph")[1], LOG_FILENAME, console_log=CONSOLE_LOG)
            
        # Save graph
        G.save_graph(os.path.join(OUTPUT_DIR, f"graph-{index}.pickle"))
        
        iteration_end = time.time()
        log_message(f"Time for iteration: {iteration_end - iteration_start:.0f}", LOG_FILENAME, console_log=CONSOLE_LOG)

        iteration_times.append(iteration_end - iteration_start)
        iteration_nodes.append(len(G.graph.nodes))
        iteration_edges.append(len(G.graph.edges))


        # Plot iteration times
        plot_iteration_times(iteration_times)
        plot_nodes_per_iteration(iteration_nodes)
        plot_edges_per_iteration(iteration_edges)
        
        
    # Save graph
    G.save_graph(os.path.join(OUTPUT_DIR, f"graph-final.pickle"))
    
    # Print execution time
    END_TIME = time.time()
    log_message(f"Execution time: {(END_TIME - START_TIME):.0f}", LOG_FILENAME, console_log=CONSOLE_LOG)
    
    # Print average iteration time
    log_message(f"Average iteration time: {np.mean(iteration_times):.0f}", LOG_FILENAME, console_log=CONSOLE_LOG)
    
    
    
    with open(os.path.join(OUTPUT_DIR, f"iteration_times.pickle"), "wb") as f:
        pickle.dump(iteration_times, f)
    with open(os.path.join(OUTPUT_DIR, f"iteration_nodes.pickle"), "wb") as f:
        pickle.dump(iteration_nodes, f)
    with open(os.path.join(OUTPUT_DIR, f"iteration_edges.pickle"), "wb") as f:
        pickle.dump(iteration_edges, f)
    

if __name__ == '__main__':
    run()