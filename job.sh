#!/bin/bash

### -- set the job Name -- 
#BSUB -J PREPROCESS

### -- Specify the output and error file. %J is the job-id --
### -- -o and -e mean append, -oo and -eo mean overwrite --

#BSUB -o logs/preprocess_%J.out
#BSUB -e logs/preprocess_%J.err
# -- end of LSF options --

### -- specify queue -- 
#BSUB -q hpc

### -- ask for number of cores -- 
#BSUB -n 1

### -- specify that the cores must be on the same host -- 
#BSUB -R "span[hosts=1]"

### -- specify that we need X GB of memory per core/slot -- 
#BSUB -R "rusage[mem=5GB]"

### -- set walltime limit: hh:mm --
#BSUB -W 24:00

### -- set the email address --
#BSUB -u s204163@student.dtu.dk
### -- send notification at start --
##BSUB -B
### -- send notification at completion--
##BSUB -N

source .env/bin/activate

python3 text-processing/preprocessing.py
