from multigroup_utilities import energy_groups

params = {}

# materials used
params['mats'] = ['abs', 'poly']

# TODO: desired lengths in units that will be defined
params['lengths'] = [1, 2]

# the wims69 energy group structure
params['eb'] = energy_groups()[::-1]*1e-6
