from multigroup_utilities import energy_groups
import numpy as np

params = {}

# reset dictionary upon rerunning?
params['reset'] = False

# materials used
params['mats'] = ['HDPE']

# length of bonner tube in cm
params['lengths'] = np.array([6])*2.54

# the wims69 energy group structure
params['eb'] = energy_groups()[::-1]*1e-6
