from graph_structure import Article, User
from batchjob_utils import log_message, memory_usage_of
import os
import pickle
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def init_articles_users(batch_files, log_file, console_log = True):
    articles = {}
    users = {}
    N = len(batch_files)
    BASEDIR = "/work3/s204163/wiki/data-batches"
    for batch_idx, batch_file in enumerate(batch_files):
        log_message(f"Index: {batch_idx} out of {N}, {batch_idx/N*100:.2f}%", log_file, console_log=console_log)
        
        with open(batch_file, 'rb') as file:
            batch = pickle.load(file)
        for index, revision in batch.iterrows():    

            article_id = str(revision["article_id"])
            user_id = str(revision["user_id"])
            
            article = articles[article_id] = articles.get(article_id, Article(article_id))
            article.user_ids.add(user_id)
            
            user = users[user_id] = users.get(user_id, User(user_id))
            user.article_ids.add(article_id)
        
        log_message(memory_usage_of(articles, "Articles")[1], log_file, console_log=console_log)
        log_message(memory_usage_of(users, "Users")[1], log_file, console_log=console_log)
        log_message(f"Number of articles: {len(articles)}", log_file, console_log=console_log)
        log_message(f"Number of users: {len(users)}", log_file, console_log=console_log)
        

            
    with open(os.path.join(BASEDIR, "articles.pickle"), "wb") as file:
        pickle.dump(articles, file)

    with open(os.path.join(BASEDIR, "users.pickle"), "wb") as file:
        pickle.dump(users, file)

def run_init_batch():
    BASEDIR = "/work3/s204163/wiki/data-batches"
    format_date = datetime.now().strftime('%Y-%m-%d.%H:%M')
    log_file = os.path.join(BASEDIR, f"init_article_user{format_date}.log")
    # # Get all batch files in directory
    batch_files = [os.path.join(BASEDIR, file) for file in os.listdir(BASEDIR) if file.startswith("batch")]
    
    init_articles_users(batch_files, log_file, console_log=True)

def article_user_plots():
    BASEDIR = "/work3/s204163/wiki/data-batches/plots"
    article_path = "/work3/s204163/wiki/data-batches/articles.pickle"
    user_path = "/work3/s204163/wiki/data-batches/users.pickle"
    
    with open(article_path, "rb") as file:
        articles = pickle.load(file)
        
    with open(user_path, "rb") as file:
        users = pickle.load(file)
        
    
    user_lengths = [len(article_lengths = [len(article.user_ids) for article in articles.values()].article_ids) for user in users.values()]
    df_user = pd.DataFrame({"user": user_lengths})
    df_article = pd.DataFrame({"article": article_lengths})
    print(df_user["user"].describe().apply("{0:.2f}".format))
    print(df_article["article"].describe().apply("{0:.2f}".format))
    
    # histplot
    ax = df_user["user"].plot.hist(bins=100)
    ax.get_figure().savefig(os.path.join(BASEDIR, "user_hist.png"))
    ax = df_article["article"].plot.hist(bins=100)
    ax.get_figure().savefig(os.path.join(BASEDIR, "article_hist.png"))
    
    # Log histplot
    ax = df_user["user"].apply(np.log).plot.hist(bins=100)
    ax.get_figure().savefig(os.path.join(BASEDIR, "user_log_hist.png"))
    ax = df_article["article"].apply(np.log).plot.hist(bins=100)
    ax.get_figure().savefig(os.path.join(BASEDIR, "article_log_hist.png"))
    
    # Boxplot
    fig, ax = plt.subplots(1, 2)
    ax[0] = df_user.plot(kind='box')
    ax[1] = df_article.plot(kind='box')
    fig.savefig(os.path.join(BASEDIR, "boxplot.png"))
    
    # Log boxplots
    fig, ax = plt.subplots(1, 2)
    ax[0] = df_user.apply(np.log).plot(kind='box')
    ax[1] = df_article.apply(np.log).plot(kind='box')
    fig.savefig(os.path.join(BASEDIR, "log_boxplot.png"))

def count_edges():
    with open("/work3/s204163/wiki/data-batches/articles.pickle", "rb") as file:
        articles = pickle.load(file)
    progressbar = tqdm(articles.values())
    
    edges = set()
    for article in progressbar:
        # An edge between two users can only be added once per article
            
        for user_id in article.user_ids:
            for user_id2 in article.user_ids:
                if user_id != user_id2:
                    edge = tuple(sorted((user_id, user_id2)))
                    edges.add(edge)
    
        # Update progressbar
        progressbar.set_description(f"Counting edges {len(edges)}", refresh=True)
        
        
    return len(edges)



if __name__ == '__main__':
    count_edges()
