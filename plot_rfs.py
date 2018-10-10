import pickle
import numpy as np
import matplotlib.pyplot as plt
from parameters import params


# import data
with open('btube_rf_data.p', 'rb') as F:
    rf = pickle.load(F)


for key, val in rf.items():
    print(key)

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylim(1e-8, 1e-2)

for key, val in rf.items():
    r, err = val.T
    ax.plot(params['eb'], r, label=key)
    # ax.errorbar(params['eb'], r, err, linestyle=None)

ax.legend()
