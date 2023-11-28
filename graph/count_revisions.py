import bz2   
import pickle
from tqdm import tqdm
from utils.read_data import groups, parse_line
import pandas as pd
import pandas as pd
import pickle
from collections import defaultdict
from batchjob_utils import log_message
import os
from datetime import datetime

filepath = "/work3/s204163/wiki/wiki-revisions-filtered.bz2"
output = "/work3/s204163/wiki/wiki-revisions-filtered-length.pickle"

# 7711541 TOTAL REVISIONS
#WARNING Mannually set, given information from a prior run, used for TQDM to show progress
N = 7711541

# Converts the bz2 file to a pandas dataframe
def create_revision_file(filepath, output, tqdm_disable = True) -> pd.DataFrame:
    log_message(f"Beginning to create revision file", output, console_log=True)
    with bz2.open(filepath, 'rt') as file:
        revisions = []
        for index, line in tqdm(enumerate(groups(file, 14)), total = N, disable=tqdm_disable):
            if index % 100000 == 0:
                log_message(f"Index: {index} out of {N}, {index/N*100:.2f}%", output, console_log=True)
            filtered_data = filter_dict_keys(parse_line(line), ['article_id', 'revision_id', 'user_id', 'article_title','username','category'])
            revisions.append(filtered_data)
    return pd.DataFrame(revisions)

# Filters a dictionary by a list of keys
def filter_dict_keys(dictionary : dict, desired_keys: list[str]):
    filtered_dict = {key: val for key, val in dictionary.items() if key in desired_keys}
    return filtered_dict

# Divides the whole dataframe into batches and saves them to a directory along with mapping files
# Such that data can be backtracked given an ID
def create_batches(df, output_dir, log_file, batch_size):
    N = len(df)
    
    # Shuffle dataframe
    df = df.sample(frac=1)
    
    # Mappings
    revision_id_map = {}
    article_id_map = defaultdict(list)
    user_id_map = defaultdict(list)
    
    log_message(f"Beginning to create batches", log_file, console_log=True)
    for i in range(0, N, batch_size):
        # Log progress
        if i % 100000 == 0: 
            log_message(f"Index: {i} out of {N}, {i/N*100:.2f}%", log_file, console_log=True)
        
        # Get batch
        if i + batch_size >= N:
            batch = df[i:]
        else:
            batch = df[i:i+batch_size]
        
        # Map ids
        for _, revision in batch.iterrows():
            revision_id = str(revision["revision_id"])
            article_id = str(revision["article_id"])
            user_id = str(revision["user_id"])
            
            revision_id_map[revision_id] = i 
            article_id_map[article_id].append(i)
            user_id_map[user_id].append(i)
        
        # save batch to outputfile{i}
        output_file = f"batch{i}.pickle"
        output_path = os.path.join(output_dir, output_file)
        batch.to_pickle(output_path)
    
    # Update mappings
    filepath = os.path.join(output_dir, "revision_id_map.pickle")
    with open(filepath, "wb") as file:
        pickle.dump(revision_id_map, file)
    
    filepath = os.path.join(output_dir, "article_id_map.pickle")
    with open(filepath, "wb") as file:
        pickle.dump(article_id_map, file)
        
    filepath = os.path.join(output_dir, "user_id_map.pickle")
    with open(filepath, "wb") as file:
        pickle.dump(user_id_map, file)
      
        
"""
This script is only run once, to create the infrastructure for the batch jobs
"""
if __name__ == '__main__':
    output_dir = "/work3/s204163/wiki/data-batches/"
    format_date = datetime.now().strftime('%Y-%m-%d.%H:%M')
    output = os.path.join(output_dir, "wiki-revisions-filtered-df.pickle")
    log_file = os.path.join(output_dir, f"count_revision{format_date}.log")
    df = create_revision_file(filepath, log_file)
    df.to_pickle(output)
    create_batches(df, output_dir, log_file, 100000)
        

        
