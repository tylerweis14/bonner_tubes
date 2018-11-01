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


class Filter_Job(object):
    """Container for a particular bonner_tube job."""
    def __init__(self, pm, l, ln, foilm, film):
        self.plug_material = pm
        self.length = l
        self.foil_material = foilm
        self.filter_material = film
        self.length_number = ln
        self.name = self.make_name()

    def make_name(self):
        """Given the properties, writes a name for the job for storage."""
        name = '{}_l{}_{}_{}'.format(self.plug_material, self.length_number, self.foil_material, self.filter_material)
        return name

    def assign_erg(self, gs, gn, el, eh):
        """Allows for the assignment for energy group stuff."""
        self.group_structure = gs
        self.group_number = gn
        self.eb = (el, eh)


def create_jobs(params):
    """This function creates the set of jobs to be ran (list) and also returns
    an empty datastructure (dict of np.arrays) that will store the response
    function data."""
    rf = {}
    jobs = []
    for m in params['mats']:
        for l_num, l in enumerate(params['lengths']):
            for foil_material in params['foils']:
                for fil in params['filters']:
                    for i, _ in enumerate(params['eb'][1:]):
                        job = Filter_Job(m, l, l_num, foil_material, fil)
                        job.assign_erg(params['group_structure'], i, params['eb'][i], params['eb'][i+1])
                        jobs.append(job)

                    # initialize empty array for rf storage and set first values to zero
                    rf[job.name] = job, np.empty((len(params['eb']), 2))
                    rf[job.name][1][0] = 0
    return jobs, rf


def master_task(params):
    # initialize data structure and create jobs
    open_jobs = []
    closed = []
    jobs, rf = create_jobs(params)

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
                rf[job.name][1][job.group_number][0] = result[0]
                rf[job.name][1][job.group_number][1] = result[1]
                closed.append(job)
                for i, open_job in enumerate(open_jobs):
                    if job.name == open_job.name and job.group_number == open_job.group_number:
                        open_jobs.remove(open_jobs[i])

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
            data = run_mcnp(job, template)
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
