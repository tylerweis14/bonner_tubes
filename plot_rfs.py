import pickle
import matplotlib.pyplot as plt
from parameters import params
from spectrum import Spectrum
from driver import Filter_Job


# import data
with open('btube_rf_data.p', 'rb') as F:
    rf = pickle.load(F)


# setup plotting environment
fig = plt.figure(0)
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylim(1e-6, 3e-2)
for key, val in rf.items():
    if 'l0' in key:
        r, err = val[1][1:].T
        xs = Spectrum(params['eb'], r, r*err)
        plot = ax.plot(*xs.stepu, label=key)
        ax.errorbar(xs.midpoints, xs.values, xs.values * err, linestyle='None', color=plot[0].get_color())

ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
          ncol=2, mode="expand", borderaxespad=0.)
