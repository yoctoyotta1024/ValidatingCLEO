"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: plot_results.py
Project: condevap
Created Date: Monday 14th April 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Wednesday 16th April 2025
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Script to plot figure 5 of S. Arabas and S. Shima 2017 using results from CLEO
0-D condensation/evaporation only box model.
"""


def displacement(time, w_avg, thalf):
    """displacement z given velocity, w, is sinusoidal
    profile: w = w_avg * pi/2 * np.sin(np.pi * t/thalf)
    where wmax = pi/2*w_avg and tauhalf = thalf/pi."""
    import numpy as np

    zmax = w_avg / 2 * thalf
    z = zmax * (1 - np.cos(np.pi * time / thalf))
    return z


def plot_one_dataset(path2pySD, axs, grid_filename, dataset, setupfile, do_plotkohler):
    ### imports
    import sys
    import numpy as np
    import random

    sys.path.append(str(path2pySD))  # for imports from pySD package
    sys.path.append(
        str(path2pySD / "examples" / "exampleplotting")
    )  # imports from example plots package

    from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat, sdtracing
    from plotssrc import as2017fig

    ### plot settings
    # w velocity [cm/s] : linewidth on plot
    lwdths = {
        100.0: 2,
        50.0: 1,
        0.2: 0.5,
    }

    ### load data
    config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=True)
    consts = pysetuptxt.get_consts(setupfile, isprint=True)
    gbxs = pygbxsdat.get_gridboxes(grid_filename, consts["COORD0"], isprint=True)
    time = pyzarr.get_time(dataset).secs
    zprof = displacement(time, config["W_avg"], config["TAU_half"])
    thermo = pyzarr.get_thermodata(dataset, config["ntime"], gbxs["ndims"], consts)
    supersat = thermo.supersaturation()

    sddata = pyzarr.get_supers(dataset, consts)
    sdid2plot = random.choice(sddata.sdId[0])  # plot one of the initial superdroplets
    attrs = ["radius", "xi", "msol"]
    sd2plot = sdtracing.attributes_for1superdroplet(sddata, sdid2plot, attrs)

    ### plot data
    w_avg = config["W_avg"] * 100
    if w_avg < 1.0:
        wlab = r"$\left< w \right>$ = {:.1f}".format(w_avg) + " cm s$^{-1}$"
    else:
        wlab = r"$\left< w \right>$ = {:.0f}".format(w_avg) + " cm s$^{-1}$"
    lwdth = lwdths[w_avg]
    lines = as2017fig.condensation_validation_subplots(
        axs, time, sd2plot["radius"], supersat[:, 0, 0, 0], zprof, lwdth=lwdth, lab=wlab
    )

    if do_plotkohler:
        as2017fig.plot_kohlercurve_with_criticalpoints(
            axs[1],
            sd2plot["radius"],
            sd2plot["msol"][0],
            thermo.temp[0, 0, 0, 0],
            sddata.IONIC,
            sddata.MR_SOL,
        )

    volume = (
        gbxs["gbxvols"][0, 0, 0] * 1e6
    )  # assuming all gbxs have same volume [/cm^3]
    xi0 = np.where(
        sddata["sdgbxindex"][0] == 0, sddata["xi"][0], 0
    )  # 0th gbx's initial droplet xi
    numconc = np.sum(xi0) / volume  # initial number concentation in volume
    textlab = (
        r"$\mathrm{N}_{\mathrm{STP}}$ = "
        + str(numconc)
        + " cm$^{-3}$\n"
        + r"r$_{\mathrm{d}}$ = "
        + "{:.2g} \u03BCm\n".format(sd2plot["radius"][0])
    )
    axs[0].text(
        0.03, 0.95, "ascent /", transform=axs[0].transAxes, fontsize=16, color="k"
    )
    axs[0].text(
        0.30, 0.95, "descent", transform=axs[0].transAxes, fontsize=16, color="orange"
    )
    axs[0].text(0.03, 0.80, textlab, transform=axs[0].transAxes, fontsize=16, color="k")

    axs[0].set_xlim([-1, 1])
    axs[0].set_ylim([0, 170])
    for ax in axs[1:]:
        ax.set_xlim([0.125, 15])
        ax.set_xscale("log")
    axs[1].set_ylim([-1, 1])
    axs[2].set_ylim([25, 75])

    for ax in axs:
        ax.spines[["right", "top"]].set_visible(False)

    return lines


def plot_results(path2pySD, grid_filename, datasets, setups):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(13, 19))

    handles, labels = [], []
    for r in range(9):
        dataset = datasets[r]
        setupfile = setups[r]
        axs = axes[:, r // 3]
        do_plotkohler = False
        if r % 3 == 0:
            do_plotkohler = True
        l1s = plot_one_dataset(
            path2pySD, axs, grid_filename, dataset, setupfile, do_plotkohler
        )
        if r < 3:
            handles.append(l1s[0])
            labels.append(l1s[0].get_label()[7:])

    ### add legends
    axes[0, 0].legend(
        handles=handles, labels=labels, loc=(0.25, 0.0), fontsize=16, frameon=False
    )
    axes[1, 0].legend(loc="upper left", fontsize=16, frameon=False)

    ### set ticks
    fsz = 16
    for ax in axes[0, :]:
        yticks = [0, 50, 100, 150]
        ax.set_yticks(yticks)
        ax.set_yticklabels([])
        ax.set_ylabel("")

        xticks = [-0.5, 0.0, 0.5]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, fontsize=fsz)
        ax.set_xlabel("$S$ /%", fontsize=fsz)
    axes[0, 0].set_ylabel("Displacement /m", fontsize=fsz)
    axes[0, 0].set_yticklabels(yticks, fontsize=fsz)

    for ax in axes[1, :]:
        yticks = [-1.0, -0.5, 0.0, 0.5, 1.0]
        ax.set_yticks(yticks)
        ax.set_yticklabels([])
        ax.set_ylabel("")

        xticks = [0.25, 1, 4, 8]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, fontsize=fsz)
        ax.set_xlabel("$R$ /\u03BCm", fontsize=fsz)
    axes[1, 0].set_ylabel("$S$ /%", fontsize=fsz)
    axes[1, 0].set_yticklabels(yticks, fontsize=fsz)

    for ax in axes[2, :]:
        yticks = [25, 50, 75]
        ax.set_yticks(yticks)
        ax.set_yticklabels([])
        ax.set_ylabel("")

        xticks = [0.25, 1, 4, 8]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, fontsize=fsz)
        ax.set_xlabel("$R$ /\u03BCm", fontsize=fsz)
    axes[2, 0].set_ylabel("Displacement /m", fontsize=fsz)
    axes[2, 0].set_yticklabels(yticks, fontsize=fsz)

    fig.tight_layout()

    return fig, axes
