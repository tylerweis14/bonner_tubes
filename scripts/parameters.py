from multigroup_utilities import energy_groups
import numpy as np

params = {}

# reset dictionary upon rerunning?
params['reset'] = True

# materials used
params['mats'] = ['HDPE']

# length of bonner tube in cm
params['lengths'] = np.array([0.0001, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]) * 2.54

# types of foils used as passive detector
params['foils'] = ['In', 'Au', 'Mo']

# types of thermal neutron filters
params['filters'] = ['', 'Cd']

# the energy group structure
params['group_structure'] = 'scale252'
params['eb'] = energy_groups(params['group_structure'])[::-1]*1e-6
params['ir_eb'] = energy_groups(params['group_structure'])[::-1]*1e-6
