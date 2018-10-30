from multigroup_utilities import energy_groups
import numpy as np

params = {}

# reset dictionary upon rerunning?
params['reset'] = False

# materials used
params['mats'] = ['HDPE']

# length of bonner tube in cm
params['lengths'] = np.array([0.001,0.25,0.5,0.75,1,1.25,1.5,1.75,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6]) * 2.54

# the wims69 energy group structure
params['eb'] = energy_groups()[::-1]*1e-6
