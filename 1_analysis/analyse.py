#!/usr/bin/env python3

import re
import subprocess

def get_simulation_results():
    with open('data.dat', 'r') as f:
        lines = f.readlines()
    
    # Group indices: 0 -- whole match, 1 -- command id, 2 -- node id, 3 -- cpu/hw thread id.
    rgx = re.compile('.*command id: command_([0-9]+), hostname: (\w+), cpu \(hw thread id\): ([0-9]+)')
    matches = [re.search(rgx, line) for line in lines]
    simulations = [{
                "command_id" : match.group(1),
                "hostname" : match.group(2),
                "cpu_id" : match.group(3)
                } for match in matches]
    
    # Need to trace each command id back to the batch it came from.
    # Determining batch id is necessary because slurm sometimes sends
    # multiple batches to same node s.t. one runs after the other.
    # This requires consideration in our analysis because otherwise
    # we can't tell cpu resuse within a batch (undesirable) from cpu
    # reuse across batches (acceptable).
    
    # Fails with Python <3.7.
    grep_output = subprocess.run(["grep command ../batch*"],
                                 capture_output=True,
                                 text=True,
                                 shell=True).stdout
    
    grep_lines = grep_output.rstrip().split('\n')
    rgx = re.compile('../batch_([0-9]+):command_([0-9]+)')
    matches = [re.search(rgx, line) for line in grep_lines]
    command_to_batch_map = {match.group(2): match.group(1) for match in matches}
    
    for sim in simulations:
        sim['batch'] = command_to_batch_map[sim['command_id']]
    return simulations

def perform_analysis():
    
    simulations = get_simulation_results()
    batch_ids = set(sim['batch'] for sim in simulations)
    
    print("Analysing result from", len(batch_ids), "batch files.")
    
    for b in batch_ids:
        print("Batch id:", b)
        relevant_sims = [s for s in simulations if s['batch'] == b]
        
        # We expect this to be one.  Let's check though.
        num_hosts = len(set([s['hostname'] for s in relevant_sims]))
        
        num_simulations_run = len(set([s['command_id'] for s in relevant_sims]))
        cpu_ids = [s['cpu_id'] for s in relevant_sims]
        num_distinct_cpus = len(set(cpu_ids))
        unused_cpu_ids = sorted([id for id in range(128) if str(id) not in cpu_ids])

        print("\t# nodes used:", num_hosts,
              ", # simulations run:", num_simulations_run,
              ", # distinct cpus used:", num_distinct_cpus,
              "\n\tunused cpus:", unused_cpu_ids)

perform_analysis()
