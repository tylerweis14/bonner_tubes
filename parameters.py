from multigroup_utilities import energy_groups
import numpy as np

params = {}

# reset dictionary upon rerunning?
params['reset'] = True

# materials used
params['mats'] = ['HDPE']

# length of bonner tube in cm
params['lengths'] = np.array([0.001, 0.25, 0.5, 0.75, 1, 1.5, 2.0, 2.5, 3.0, 4.0, 6]) * 2.54

# the wims69 energy group structure
params['eb'] = energy_groups()[::-1]*1e-6
