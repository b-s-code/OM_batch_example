#!/usr/bin/env python3

import sys
import ctypes
import time

def get_cpu_id():
    """
    The sched_getcpu system call may report a higher value than
    the number of CPU cores availabe on a machine.  Each work
    partition node on Setonix has 2X 64-core AMD EPYC 7763 CPUs.
    AMD EPYC 7763 supports 2-way SMT, so effectively there are
    256 hardware threads per node.  This number, 256, is consistent
    with the range of values returned by sched_getcpu in practice.
    So, probably, sched_getcpu is returning a hardware thread ID.
    """
    libc = ctypes.CDLL("libc.so.6")
    cpu_id = libc.sched_getcpu()
    return cpu_id

def get_hostname():
    """
    The output for the command `hostname` should be passed as the
    first argument to this script.  The environment variable
    HOSTNAME should not be used because it can be inherited from a
    login node by a work node on a HPC system.  `hostname` does
    not appear to have this same issue.
    """
    hostname = sys.argv[1]
    return hostname

def get_command_id():
    """
    The command id number should be passed as the second argument
    to this script.
    """
    command_id = sys.argv[2]
    return command_id

def main():
    assert(len(sys.argv) == 3)
    cpu_id = get_cpu_id()
    hostname = get_hostname()
    command_id = get_command_id()
    print(f"command id: {command_id}, hostname: {hostname}, cpu (hw thread id): {cpu_id}")

    # Sleep so that Slurm or OS does not a reuse CPU which process has finished using.
    time.sleep(30)

if __name__ == "__main__":
    main()

