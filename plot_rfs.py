import pickle
import numpy as np
import matplotlib.pyplot as plt
from parameters import params
from spectrum import Spectrum


# import data
with open('btube_rf_data.p', 'rb') as F:
    rf = pickle.load(F)


for key, val in rf.items():
    print(key)

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylim(1e-9, 1e-2)

for key, val in rf.items():
    if 'poly' in key:
        r, err = val[1:].T
        xs = Spectrum(params['eb'], r, err)
        plot = ax.plot(*xs.stepu, label=key)
        #ax.errorbar(xs.midpoints, xs.values, xs.error, color=plot[0].get_color(), linestyle='None')

ax.legend()
