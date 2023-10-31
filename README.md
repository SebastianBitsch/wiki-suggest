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

### Useful Commands

```
getquota_zhome.sh
```
```
module avail
module list
module load
```
### Notes
- Since HPC already has a lot of packages, it is often easier to just to: ```module load ...``` 
- Data is stored in /work3/s204163/
- 

### Reading chunks of large files
```python
import bz2

CHUNK_SIZE = 1024 * 1024 * 1024 # 1GB

with bz2.BZ2File('/work3/s204163/enwiki-20080103.main.bz2', 'r') as f:
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:  # End of file
            break
        # Process chunk here, e.g., parse the lines and analyze the data
        lines = chunk.decode('utf-8').split('\n')
        for line in lines:
            pass
```

```python
chunk_iter = pd.read_csv("/work3/s204163/enwiki-20080103.main.bz2", compression='bz2', chunksize = CHUNK_SIZE, delimiter='\t', ...)

for chunk_df in chunk_iter:
    pass

```