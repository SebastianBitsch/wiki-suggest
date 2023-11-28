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
from collections import defaultdict

sns.set_theme(style="darkgrid")


path = '/work3/s204163/wiki/data-batches/wiki-revisions-filtered-df.pickle'
log = '/work3/s204163/wiki/data-batches/df_stats_log.txt'
with open(path, 'rb') as f:
    df = pickle.load(f)

category_count = defaultdict(int)
category_article = defaultdict(set)
N = len(df)

# Count category references given revisions or articles
for index, revision in tqdm(df.iterrows(), total=N, disable = True):
    for category in revision['category']:
        category_count[category] += 1
        category_article[revision['article_id']].add(category)
        
    if index % 100000 == 0:
        log_message(f"Index: {index//100000} out of {N//100000} [{index//N*100}%]", log, console_log=False)
        
with open('/work3/s204163/wiki/data-batches/category_count.pickle', 'wb') as f:
    pickle.dump(category_count, f)

with open('/work3/s204163/wiki/data-batches/category_article.pickle', 'wb') as f:
    pickle.dump(category_article, f)