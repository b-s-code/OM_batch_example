#!/bin/bash -l

# INSTRUCTIONS on using this script.
# 1. Run 128+ simulations on a single node using relevant scenario files - measure duration.
# 2. Make a decision about how many nodes to request for production run (tradeoff: queuing time for many nodes is high, execution time with few nodes is high).
# 3. Do a quick calculation to work out value of NUM_SIMULATIONS_PER_NODE required to use decided number of nodes.
# 4. Set value in script and run.

# Can be >128.
# To scale up number of simulations, this is
# the number to increase, ideally with a multiple of 128.
# This can be used to scale past limit imposed
# by maximum number of concurrent jobs, or
# to reduce queuing time.
NUM_SIMULATIONS_PER_NODE=128

# Note that this step creates one file per batch.
split -l ${NUM_SIMULATIONS_PER_NODE} -d ./input_params.txt batch_

for batch in batch_*; do
    sbatch --export=PARAMS_LIST=$batch om_batch.sh
done
