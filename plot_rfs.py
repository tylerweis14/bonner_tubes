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
ax.plot(params['eb'], rf['poly_1cm'][:, 0])
