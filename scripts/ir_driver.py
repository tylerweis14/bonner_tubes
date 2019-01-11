import numpy as np
import pickle
from driver import Filter_Job
from mcnp_template import template
from run_mcnp import run_mcnp
from parameters import params
from time import time


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
                    job = Filter_Job(m, l, l_num, foil_material, fil, job_type='ir')
                    jobs.append(job)

                    # initialize empty array for rf storage and set first values to zero
                    rf[job.name] = job, np.zeros((len(params['ir_eb']), 2)), np.zeros(2)
                    rf[job.name][1][0] = 0
    return jobs, rf


def master_task(params):
    """Creates jobs and then runs them for the integral responses."""

    # first, create the jobs
    jobs, rf = create_jobs(params)

    # do your job
    for job in jobs:
        results = run_mcnp(job, template)
        rf[job.name][1][:, 0] = results[0]
        rf[job.name][1][:, 1] = results[1]
        rf[job.name][2][0] = results[2]
        rf[job.name][2][1] = results[3]

    # update stored data
    try:
        with open('btube_ir_data.p', 'rb') as F:
            database = pickle.load(F)
            if params['reset']:
                database = {}
            database.update(rf)
    except:
        database = {}
        database.update(rf)
    with open('btube_ir_data.p', 'wb') as F:
        pickle.dump(database, F)
    return


if __name__ == '__main__':
    start_time = time()
    master_task(params)
    end_time = time()
    msg = 'Script Ran in {:6.2e} s:'.format(end_time - start_time)
    with open('runtime_info.txt', 'w+') as F:
        F.write(msg)
