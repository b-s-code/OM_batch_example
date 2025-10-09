#!/bin/bash -l

# Can be >128.
NUM_SIMULATIONS_PER_NODE=128

# Note that this step creates one file per batch.
split -l ${NUM_SIMULATIONS_PER_NODE} -d ./input_params.txt batch_

for batch in batch_*; do
    sbatch --export=PARAMS_LIST=$batch om_batch.sh
done
