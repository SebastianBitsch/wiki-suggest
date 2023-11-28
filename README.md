# wiki-suggest
*This is an exam project for cource 02807 Computational Tools for Data Science.*

In this repository you will find an implementation of a recommendation engine for editors of Wikipedia. The purpose is to help editors make better decisions about what article they should edit next, taking into consideration what articles they have previosuly edited.

The recommendation engine consists of two equal parts that together form a recommendation for a given user;
1. **Articles most similar to the ones you have edited previously.** 
    All code related to this is in the `text-processing/` directory
    - End to end recommendation based on what articles a user has edited is done in `recommend.py`
    - Preprocessing to create feature vectors, clusters, etc. is done in `preprocessing.py`
    - TF-IDF is implemented in `TFIDF.py`
    - K-Means is implemented in `kmeans.py`
    - DBSCAN is implemented in `dbscan.py`
    - Notebooks generally contain exploratory analysis and plotting

2. **Articles other people like you have edited**
    All code related to this is in the `graph/` directory
    - Structuring of the social graph and it's class methods can be found in 'graph_structure.py' which is the backbone of the social graphs
    - Most of the files are utility functions for the graph structure used for faster, more memory efficient batchjobs
    - spectral_clustering_from_scratch.py is a file containing a spectral clustering algorithm implemented from scratch
    - modularity_test.ipynb is a modularity test also implemented from scratch.
    - The girvan_newman implementation can be found at graph_girvan_newman.py
    - Due to the nature of large social graph, one has to carefully analyse the graph structure before construction in order to balance the amount of Nodes and Edges. create_graph.py create a social graph with only editors/users as nodes, meanwhile create_graph_articles creates a bi-partite social graph with editors/users and articles as nodes. The latter is used for the recommendation engine.



## Practicals

### Getting started

1. Load python3.10 from HPC [list of modules](https://www.hpc.dtu.dk/?page_id=282)
```bash
module load python3/3.10.7
module load matplotlib/3.6.0-numpy-1.23.3-python-3.10.7
```
2. Create virtual enviornment
```bash
python3 -m venv .env
```
```bash
source .env/bin/activate
```
```bash
python -m pip  install -r requirements.txt
```

3. Paste common modules into bin/activate file to automatically load every session
```bash
module load python3/3.10.7
module load pandas/1.4.4-python-3.10.7
...
```

4. To make imports across folders possible we are using a `setup.py` and `__init__.py` files. Install using:
```bash
pip install -e .
```

### Data on scratch
#### Datasets
- [wikipedia-good-articles.zip](https://www.kaggle.com/datasets/jacksoncrow/wikipedia-multimodal-dataset-of-good-articles/data)
    - collection of good articles (i.e. they have text). We are interested in the article-id, title and text.
- [wikipedia-revisions-dataset.bz2](https://snap.stanford.edu/data/wiki-meta.html)
    - huge dataset that contains 14 row per revision with a lot of data.
#### Wrangled data
- article_ids:
    - list of ids for every article that has text (i.e. is in good-articles.zip)
- article_texts:
    - dictionary of article_id : title + text, for every article that has text (i.e. is in good-articles.zip)
- index_file:
    - dictionary of revision number : byte location. For every 1000 revisions a byte location the byte location at that revision is stored - makes random access much much faster.

### Useful Commands

```
getquota_zhome.sh
du -h --max-depth=1 --apparent $HOME
```
```
module avail
module list
module load
```
### Notes
- Since HPC already has a lot of packages, it is often easier to just to: ```module load ...``` 
- Data is stored in /work3/s204163/wiki
- For printing a couple of lines (for debugging etc.) use the command ```bzcat /work3/s204163/wiki/wiki-revisions-dataset.bz2 | head -n 4902767 | tail -n 4```. Prints line 4902767 - 4902771
- Get the number of lines with ```bzcat /work3/s204163/wiki/wiki-revisions-dataset.bz2 | wc -l```. Took +4 hours, result: 1632271984 lines
- See access right of ```ls -ld /work3/s204163```. Refer to [this table](https://askubuntu.com/a/409104) to see rights
