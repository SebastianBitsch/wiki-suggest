from graph_structure import Article
import random
from tqdm import tqdm # Progress Bar

def get_batches(N, batch_size) -> int:
    random.sample(range(N), )

def gather_articles(N, batch_size, **kwargs) -> dict:
    kwargs.get("log_file", None)
    kwargs.get("console_log", False)
    kwargs.get("tqdm_disable", True)
    kwargs.get("log_interval", None)
    
    articles = {}
    
    df_revisions = read_revisions(file_path, N=N)
    
print(get_batches(100, 10))