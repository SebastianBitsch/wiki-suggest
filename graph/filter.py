import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

BASEDIR = "/work3/s204163/wiki/data-batches/"
user_path = "/work3/s204163/wiki/data-batches/users.pickle"


with open(user_path, "rb") as f:
    users = pickle.load(f)
    
    
user_percentiles = list(map(int, np.percentile(user_lengths, percentiles)))


# article_path = "/work3/s204163/wiki/data-batches/articles.pickle"

# with open(article_path, "rb") as f:
#     articles = pickle.load(f)