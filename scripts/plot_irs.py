import numpy as np
import pickle
import matplotlib.pyplot as plt
from parameters import params
from spectrum import Spectrum
from driver import Filter_Job


# import data
with open('btube_ir_data.p', 'rb') as F:
    ir = pickle.load(F)


def plot_saturated_activities(keys, params, savename):
    """Plots the saturated activities of the integral responses."""

    # grab the lengths from the parameters
    lengths = params['lengths']

    # initialize arrays for activity and error
    act = np.empty(len(lengths))
    err = np.empty(len(lengths))

    # loop through activities
    for i, key in enumerate(keys):
        act[i] = ir[key][2][0]
        err[i] = ir[key][2][1]

    # normalize data to flux at 1kW
    act *= 2.949E+05 * (1000 / 250) * (np.pi * 0.9525**2)

    # convert from Bq to uCi
    act *= (1 / 3.7E4)

    # change err from relative to absolute
    err = err * act

    # set up plotting environment
    fig = plt.figure(0)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Length $cm$')
    ax.set_ylabel('Saturated Activity $\mu Ci$')
    ax.set_yscale('log')
    ax.set_ylim(8E-2, 2E3)

    # plot values
    ax.plot(lengths, act, ls='None', c='k', marker='o', ms=3, label=keys[0])
    ax.errorbar(lengths, act, err, c='k', ls='None')

    # add legend
    ax.legend()

    # save and then clear figure
    fig.savefig('../img/' + savename + '.png', dpi=300)
    fig.clf()

    return


def plot_roi(keys, params, savename):
    """Plots the 5% and 95% cutoffs for each response function."""

    # create some height values
    heights = np.logspace(-10, 1, len(keys))

    # nebp spectrum
    nebp_erg, nebp_flux, _ = np.loadtxt('nebp_spectrum.txt', unpack=True)
    nebp = Spectrum(nebp_erg, nebp_flux[1:])

    # create plotting environment
    fig0 = plt.figure(0)
    ax0 = fig0.add_subplot(111)
    ax0.set_xlabel('Energy $MeV$')
    ax0.set_ylabel('$\Phi$ Arbitrary Units')
    ax0.set_xscale('log')
    ax0.set_yscale('log')
    ax0.set_xlim(1e-11, 20)

    # create cumsum plotting environment
    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111)
    ax1.set_xlabel('Energy $MeV$')
    ax1.set_ylabel('Cumulative Fractional Response')
    ax1.set_xscale('log')
    ax1.set_xlim(1e-11, 20)

    # plot nebp spectrum
    ax0.plot(*nebp.step, c='k', lw=0.7)

    for i, key in enumerate(keys):
        # random key (change later)
        val = ir[key]
        spectral_resp = val[1][:, 0]

        # calculate the cumulative sum
        cumsum = np.cumsum(spectral_resp / np.sum(spectral_resp))

        # calculate energy bounds
        bounds = np.interp(0.05, cumsum, params['ir_eb']), np.interp(0.95, cumsum, params['ir_eb'])

        # plot data
        ax0.plot(bounds, [heights[i]]*2)

        # make spectrum for cumsum plot
        csum = Spectrum(params['ir_eb'], cumsum[1:])
        ax1.plot(*csum.stepu, lw=0.5, label=key)

    # legend
    ax0.legend()
    ax1.legend()

    # save and clear figure
    fig1.savefig('../img/' + savename + '.png', dpi=300)
    fig1.clf()
    fig0.clf()


keys0 = []
keys1 = []
keys2 = []
keys3 = []
keys4 = []
keys5 = []
for key in ir.keys():
    if 'In' in key and 'Cd' not in key:
        keys0.append(key)
    if 'In' in key and 'Cd' in key:
        keys1.append(key)
    if 'Au' in key and 'Cd' not in key:
        keys2.append(key)
    if 'Au' in key and 'Cd' in key:
        keys3.append(key)
    if 'Mo' in key and 'Cd' not in key:
        keys4.append(key)
    if 'Mo' in key and 'Cd' in key:
        keys5.append(key)


plot_saturated_activities(keys0, params, 'sat_In')
plot_roi(keys0, params, 'roi_In')

plot_saturated_activities(keys1, params, 'sat_InCd')
plot_roi(keys1, params, 'roi_InCd')

plot_saturated_activities(keys2, params, 'sat_Au')
plot_roi(keys2, params, 'roi_Au')

plot_saturated_activities(keys3, params, 'sat_AuCd')
plot_roi(keys3, params, 'roi_AuCd')

plot_saturated_activities(keys4, params, 'sat_Mo')
plot_roi(keys4, params, 'roi_Mo')

plot_saturated_activities(keys5, params, 'sat_MoCd')
plot_roi(keys5, params, 'roi_MoCd')
