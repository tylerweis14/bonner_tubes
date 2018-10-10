import numpy as np
import pickle
from parameters import params
from mcnp_template import template
from run_mcnp import run_mcnp
from time import time
from mpi4py import MPI
# Initializations and preliminaries
comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.size        # total number of processes
rank = comm.rank        # rank of this process
status = MPI.Status()   # get MPI status object


tags = {'REQUEST': 1,
        'INQUIRE': 2,
        'STATUS': 3,
        'JOB': 4,
        'DATA': 5}


def master_task(params):
    # initialize data structure and create jobs
    rf = {}
    jobs = []
    open_jobs = []
    closed = []
    for m in params['mats']:
        for l in params['lengths']:
            name = '{}_{}cm'.format(m, l)
            rf[name] = np.empty((len(params['eb']), 2))
            rf[name][0] = 0
            for i, _ in enumerate(params['eb'][1:]):
                jobs.append((name+str(i), (params['eb'][i], params['eb'][i+1]), m, l, template))

    # distribute work
    slave_exit_status = [False] * size
    slave_exit_status[0] = True
    while True:
        # find slave and establish communication
        ready_node = comm.recv(source=MPI.ANY_SOURCE, tag=tags['REQUEST'])
        comm.send(ready_node, dest=ready_node, tag=tags['INQUIRE'])
        slave_status = comm.recv(source=ready_node, tag=tags['STATUS'])

        if jobs or slave_status == 'COMPLETE':
            if slave_status == 'IDLE':
                next_job = jobs.pop()
                comm.send(next_job, ready_node, tag=tags['JOB'])
                open_jobs.append(next_job)
            elif slave_status == 'COMPLETE':
                job, result = comm.recv(source=ready_node, tag=tags['DATA'])
                s = job[0].split('cm')
                name = s[0] + 'cm'
                i = int(s[1])
                rf[name][i][0] = result[0]
                rf[name][i][1] = result[1]
                closed.append(job)
                open_jobs.remove(job)

        # tell slaves to quit
        elif not jobs and slave_status == 'IDLE':
            comm.send('QUIT', dest=ready_node, tag=tags['JOB'])
            slave_exit_status[ready_node] = True
            if False in slave_exit_status:
                pass
            else:
                break

    # update stored data
    with open('btube_rf_data.p', 'rb') as F:
        database = pickle.load(F)
        if params['reset']:
            database = {}
        database.update(rf)
    with open('btube_rf_data.p', 'wb') as F:
        pickle.dump(database, F)
    return


def slave_task():
    status = 'IDLE'
    while True:
        # establish communciation with master
        comm.send(rank, dest=0, tag=tags['REQUEST'])
        comm.recv(source=0, tag=tags['INQUIRE'])

        # let master know status
        comm.send(status, dest=0, tag=tags['STATUS'])

        # recieve job from master
        if status == 'IDLE':
            job = comm.recv(source=0, tag=tags['JOB'])
            if job == 'QUIT':
                break
            status = 'BUSY'
            data = run_mcnp(*job)
            status = 'COMPLETE'
        elif status == 'COMPLETE':
            comm.send((job, data), dest=0, tag=tags['DATA'])
            status = 'IDLE'
    return


if __name__ == '__main__':
    if rank == 0:
        start_time = time()
        master_task(params)
        end_time = time()
        msg = 'Script Ran in {:6.2e} s:'.format(end_time - start_time)
        with open('runtime_info.txt', 'w+') as F:
            F.write(msg)
    else:
        slave_task()
