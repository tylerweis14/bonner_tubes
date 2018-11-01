from multigroup_utilities import energy_groups
import numpy as np

params = {}

# reset dictionary upon rerunning?
params['reset'] = True

# materials used
params['mats'] = ['HDPE']

# length of bonner tube in cm
params['lengths'] = np.array([0.001, 0.5]) * 2.54

# types of foils used as passive detector
params['foils'] = ['In']

# types of thermal neutron filters
params['filters'] = ['', 'Cd']

# the wims69 energy group structure
params['group_structure'] = 'wims69'
params['eb'] = energy_groups()[::-1]*1e-6
