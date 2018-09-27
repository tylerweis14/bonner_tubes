from master_slave import master_task, slave_task
from mpi4py import MPI
# Initializations and preliminaries
comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.size        # total number of processes
rank = comm.rank        # rank of this process
status = MPI.Status()   # get MPI status object

if rank == 0:
    master_task()
else:
    slave_task()
