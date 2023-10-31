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
