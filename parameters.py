from multigroup_utilities import energy_groups

params = {}

# reset dictionary upon rerunning?
params['reset'] = True

# materials used
params['mats'] = ['poly']

# length of bonner tube in cm
params['lengths'] = [10, 15]

# the wims69 energy group structure
params['eb'] = energy_groups()[::-1]*1e-6
