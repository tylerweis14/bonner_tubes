import pickle
import matplotlib.pyplot as plt
from parameters import params
from spectrum import Spectrum
from driver import Filter_Job


# import data
with open('btube_rf_data.p', 'rb') as F:
    rf = pickle.load(F)


def plot_rf(i, condition, savename):
    # setup plotting environment
    fig = plt.figure(i)
    ax = fig.add_subplot(111)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Energy MeV')
    ax.set_ylabel('Response Function')
    ax.set_ylim(1e-6, 3e-2)
    for key, val in rf.items():
        if condition(key):
            r, err = val[1][1:].T
            xs = Spectrum(params['eb'], r, r*err)
            plot = ax.plot(*xs.stepu, label=key, lw=0.7)
            # ax.errorbar(xs.midpoints, xs.values, xs.values * err, linestyle='None', color=plot[0].get_color(), lw=0.7)

    leg = ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                    ncol=2, mode="expand", borderaxespad=0.)
    fig.savefig('../img/' + savename + '.png', dpi=300, bbox_extra_artists=(leg,), bbox_inches='tight')


# bare responses
plot_rf(0, lambda k: ('In' in k and 'Cd' not in k and 'Gd' not in k), 'indium_bare')
plot_rf(1, lambda k: ('Au' in k and 'Cd' not in k and 'Gd' not in k), 'gold_bare')
plot_rf(2, lambda k: ('Mo' in k and 'Cd' not in k and 'Gd' not in k), 'moly_bare')

# cd responses
plot_rf(3, lambda k: ('In' in k and 'Cd' in k), 'indium_cd')
plot_rf(4, lambda k: ('Au' in k and 'Cd' in k), 'gold_cd')
plot_rf(5, lambda k: ('Mo' in k and 'Cd' in k), 'moly_cd')

# gcd responses
#plot_rf(6, lambda k: ('In' in k and 'Gd' in k), 'indium_gd')
#plot_rf(7, lambda k: ('Au' in k and 'Gd' in k), 'gold_gd')
#plot_rf(8, lambda k: ('Mo' in k and 'Gd' in k), 'moly_gd')
