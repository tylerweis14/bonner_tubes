import numpy as np
from mcnp_template import template
from run_mcnp import run_mcnp
from multigroup_utilities import energy_groups
from mpi4py import MPI
# Initializations and preliminaries
comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.size        # total number of processes
rank = comm.rank        # rank of this process
status = MPI.Status()   # get MPI status object


def master_task():
    # parameters
    mats = ['abs', 'poly']
    lengths = [1, 2, 3, 4, 5]
    eb = energy_groups()[::-1]*1e-6

    # initialize data structure and create jobs
    rf = {}
    jobs = []
    open_jobs = []
    closed = []
    for m in mats:
        for l in lengths:
            name = '{}_{}cm'.format(m, l)
            rf[name] = np.empty((len(eb), 2))
            rf[name][0] = 0
            for i, _ in enumerate(eb[1:]):
                jobs.append((name+str(i), (eb[i], eb[i+1]), m, l, template))

    # distribute work
    slave_exit_status = [False] * size
    slave_exit_status[0] = True
    while True:
        # find slave and establish communication
        ready_node = comm.recv(MPI.ANY_SOURCE, tag='REQUEST')
        comm.send(ready_node, tag='INQUIRE')
        slave_status = comm.recv(ready_node, tag='STATUS')

        if jobs or open_jobs:
            if slave_status == 'IDLE':
                next_job = jobs.pop()
                comm.send(next_job, ready_node, tag='JOB')
                open_jobs.append(next_job)
            elif slave_status == 'COMPLETE':
                job, result = comm.recv(ready_node, tag='DATA')
                name = '{}_{}cm'.format(job[0], job[1])
                rf[name][0] = result[0]
                rf[name][1] = result[1]
                closed.append(job)
                open_jobs.remove(job)

        # tell slaves to quit
        else:
            comm.send('QUIT', dest=i, tag=i)
            slave_exit_status[i] = True
            if False in slave_exit_status:
                pass
            else:
                break
    return


def slave_task():
    status = 'IDLE'
    while True:
        # establish communciation with master
        comm.send(rank, dest=0, tag='REQUEST')
        comm.recv(0, tag='INQUIRE')

        # let master know status
        comm.send(status, 0, tag='STATUS')

        # recieve job from master
        if status == 'IDLE':
            job = comm.recv(source=0, tag='JOB')
            if job == 'QUIT':
                break
            status = 'BUSY'
            data = run_mcnp(*job)
            status = 'COMPLETE'
        elif status == 'COMPLETE':
            comm.send(data, dest=0, tag='DATA')
            status = 'IDLE'
    return
