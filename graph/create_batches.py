import pandas as pd
import pickle
from collections import defaultdict

def create_batches(filepath, outputfile, batch_size):
    df = pd.read_pickle(filepath)
    N = len(df)
    
    # Shuffle dataframe
    df = df.sample(frac=1)
    
    revision_id_map = {}
    article_id_map = defaultdict(list)
    user_id_map = defaultdict(list)
    
    for i in range(0, N, batch_size):
        revision_id_map[df[i]["revision_id"]] = i 
        article_id_map[df[i]["article_id"]].append(i)
        user_id_map[df[i]["user_id"]].append(i)
        
        batch = df[i:i+batch_size]
        
        # save batch to outputfile{i}
        output = f"outputfile{i}"
        batch.to_pickle(output)
        
        
        
        