from bonner_tube_template import template
import numpy as np
from multigroup_utilities import energy_groups
s = template
eb = energy_groups()[::-1]*1e-6
n = len(eb)
for i in range(n-1):
    s = s.format(eb[i],eb[i+1])
    print(s)