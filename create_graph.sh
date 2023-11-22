#!/bin/bash

### -- set the job Name -- 
#BSUB -J CREATE_GRAPH

### -- Specify the output and error file. %J is the job-id --
### -- -o and -e mean append, -oo and -eo mean overwrite --

#BSUB -o /work3/s204163/wiki/graph_logs/hpc/create_graph_userV2_%J.out
#BSUB -e /work3/s204163/wiki/graph_logs/hpc/create_graph_userV2_%J.err
# -- end of LSF options --

### -- specify queue -- 
#BSUB -q hpc

### -- ask for number of cores -- 
#BSUB -n 1

### -- specify that the cores must be on the same host -- 
#BSUB -R "span[hosts=1]"

### -- specify that we need X GB of memory per core/slot -- 
#BSUB -R "rusage[mem=32GB]"

### -- set walltime limit: hh:mm --
#BSUB -W 24:00

### -- set the email address --
###BSUB -u s204115@student.dtu.dk
### -- send notification at start --
##BSUB -B
### -- send notification at completion--
##BSUB -N

source .venv/bin/activate
python3 graph/create_graph.py
