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
ax.set_ylim(1e-10, 1)

lengths = [6*2.54]
for key, val in rf.items():
    num = float(key.split('_')[1][:-2])
    if 'HDPE' in key and num in lengths:
        r, err = val[1:].T
        xs = Spectrum(params['eb'], r, r*err)
        plot = ax.plot(*xs.stepu, label=key)
        ax.errorbar(xs.midpoints, xs.values, xs.error, color=plot[0].get_color(), linestyle='None')

ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
