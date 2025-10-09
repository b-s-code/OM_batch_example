#!/bin/bash -l

# Can be >128.
NUM_SIMULATIONS_PER_NODE=128

# Seems like this will create many files.
# TODO: check.
split -l ${NUM_SIMULATIONS_PER_NODE} -d ${MYSCRATCH}/input_params.txt batch_

for batch in batch_*; do
    sbatch --export=PARAMS_LIST=$batch om_batch.sh
done
