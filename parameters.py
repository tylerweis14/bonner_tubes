from multigroup_utilities import energy_groups

params = {}

# reset dictionary upon rerunning?
params['reset'] = False

# materials used
params['mats'] = ['poly', 'abs']

# length of bonner tube in cm
params['lengths'] = [1, 2, 3, 4, 5, 8, 10, 15, 20, 25]

# the wims69 energy group structure
params['eb'] = energy_groups()[::-1]*1e-6
