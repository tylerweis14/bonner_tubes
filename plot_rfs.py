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
ax.set_ylim(1e-7, 1e-2)

lengths = [1, 2, 3, 4, 5, 8]
for key, val in rf.items():
    num = float(key[5:-2])
    if 'poly' in key and num in lengths:
        r, err = val[1:].T
        xs = Spectrum(params['eb'], r, r*err)
        plot = ax.plot(*xs.stepu, label=key)
        ax.errorbar(xs.midpoints, xs.values, xs.error, color=plot[0].get_color(), linestyle='None')

ax.legend()
