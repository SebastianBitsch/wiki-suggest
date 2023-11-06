# wiki-suggest

## Practicals

### Getting started

1. Load python3.10 from HPC [list of modules](https://www.hpc.dtu.dk/?page_id=282)
```bash
module load python3/3.10.7
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
