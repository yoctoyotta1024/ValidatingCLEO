"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: plot_results.py
Project: collisions
Created Date: Wednesday 16th April 2025
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
Script to plot figure similar to figure 2 of Shima et al. 2009
using results from CLEO 0-D collisions-only box model.
"""


def plot_massdendistrib(
    path2pySD, sdgbxindex, radius, xi, gbxs, sddata, nbins, rspan, smoothsig
):
    import sys
    import numpy as np

    sys.path.append(
        str(path2pySD / "examples" / "exampleplotting")
    )  # imports from example plots package
    from plotssrc import shima2009fig

    gbx2plt = 0  # plot 0th gridbox
    volume = gbxs["gbxvols"][0, 0, 0]  # assuming all gbxs have same volume [m^3]

    radius = np.where(sdgbxindex == gbx2plt, radius, np.nan)
    xi = np.where(sdgbxindex == gbx2plt, xi, np.nan)

    hist, hcens = shima2009fig.calc_massdens_distrib(
        rspan, nbins, volume, xi, radius, sddata, smoothsig
    )

    return hist, hcens


def plot_massdendistrib_evolution(
    path2pySD, ax, grid_filename, times2plot, datasets2plot, setups2plot, kernellabels
):
    import sys
    import awkward as ak
    import numpy as np

    sys.path.append(str(path2pySD))  # for imports from pySD package
    from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat, sdtracing

    ### kernel: line [label, style]
    lstyles = {
        "Golovin 1963": [
            "G1963",
            "-.",
        ],
        "Long 1974": [
            "L1974",
            "-",
        ],
        "Testik 2011 + Straub 2010": [
            "T2011+S2010",
            "--",
        ],
    }
    ### nsupers: line width
    lwidths = {
        8192: 1.0,
        131072: 2.0,
        2097152: 3.0,
    }

    khandles, klabels = [], []
    for dataset, setupfile, kernel in zip(datasets2plot, setups2plot, kernellabels):
        ### read in constants and intial setup from setup .txt file
        consts = pysetuptxt.get_consts(setupfile, isprint=True)
        gbxs = pygbxsdat.get_gridboxes(grid_filename, consts["COORD0"], isprint=True)

        # read in output Xarray data
        time = pyzarr.get_time(dataset).secs
        sddata = pyzarr.get_supers(dataset, consts)

        smoothsig_factor = 0.62
        nsupers0 = np.sum(
            np.where(sddata.sdgbxindex[0] == 0, 1, 0)
        )  # initial num superdrops in 0th gbx
        smoothsig = smoothsig_factor * (
            nsupers0 ** (-1 / 5)
        )  # = ~0.2 for guassian smoothing

        nbins = 500
        non_nanradius = ak.nan_to_none(sddata["radius"])
        rspan = [ak.min(non_nanradius), ak.max(non_nanradius)]

        attrs2sel = ["sdgbxindex", "radius", "xi"]
        sddata2plot = sdtracing.attributes_at_times(sddata, time, times2plot, attrs2sel)

        tcolors, tlabels = [], []
        for n, t2plt in enumerate(times2plot):
            ind = np.argmin(abs(time - t2plt))
            tlab = "t = {:.0f}s".format(time[ind])
            color = "C" + str(n)

            sdgbxindex = sddata2plot["sdgbxindex"][n]
            radius = sddata2plot["radius"][n]
            xi = sddata2plot["xi"][n]
            nsupers = len(sdgbxindex)

            mass = (
                np.sum(1000.0 * 4.0 / 3.0 * (radius / 1e6) ** 3 * np.pi * xi)
                * 1000
                / 1e6
            )
            print(f"mass of water in domain = {mass} g cm-3")

            hist, hcens = plot_massdendistrib(
                path2pySD, sdgbxindex, radius, xi, gbxs, sddata, nbins, rspan, smoothsig
            )

            # for legend
            if n == 0:
                kline = ax.plot(
                    hcens,
                    hist,
                    color="k",
                    linestyle=lstyles[kernel][1],
                    linewidth=lwidths[nsupers],
                    zorder=0,
                )[0]
                khandles.append(kline)
                klabels.append(lstyles[kernel][0] + ", N$_{SD}$=" + str(nsupers))

            ax.plot(
                hcens,
                hist,
                color=color,
                linestyle=lstyles[kernel][1],
                linewidth=lwidths[nsupers],
            )[0]
            tcolors.append(color)
            tlabels.append(tlab)

    y = 0.95
    for tlab, color in zip(tlabels, tcolors):
        ax.text(0.03, y, tlab, transform=ax.transAxes, color=color)
        y -= 0.055
    ax.legend(handles=khandles, labels=klabels)


def plot_results(path2pySD, grid_filename, datasets, setups):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(6, 12))

    ### plot golovin kernel datasets
    times2plot = [0, 1200, 2400, 3600]
    datasets2plot = [datasets[0], datasets[1]]
    setups2plot = [setups[0], setups[1]]
    kernellabels = ["Golovin 1963"] * 2
    plot_massdendistrib_evolution(
        path2pySD,
        axes[0],
        grid_filename,
        times2plot,
        datasets2plot,
        setups2plot,
        kernellabels,
    )

    ### plot long and testikstraub datasets version 1
    times2plot = [0, 600, 1200, 1800]
    datasets2plot = [datasets[2], datasets[4], datasets[3], datasets[5]]
    setups2plot = [setups[2], setups[3], setups[4], setups[5]]
    kernellabels = ["Long 1974", "Testik 2011 + Straub 2010"] * 2
    plot_massdendistrib_evolution(
        path2pySD,
        axes[1],
        grid_filename,
        times2plot,
        datasets2plot,
        setups2plot,
        kernellabels,
    )

    ### plot long and testikstraub datasets version 2
    times2plot = [0, 1200, 2400, 3600]
    datasets2plot = [datasets[6], datasets[8], datasets[7], datasets[9]]
    setups2plot = [setups[6], setups[7], setups[8], setups[9]]
    kernellabels = ["Long 1974", "Testik 2011 + Straub 2010"] * 2
    plot_massdendistrib_evolution(
        path2pySD,
        axes[2],
        grid_filename,
        times2plot,
        datasets2plot,
        setups2plot,
        kernellabels,
    )

    ### beautify axes
    for ax in axes:
        ax.set_xscale("log")
        ax.set_xlim([10, 5000])
        ax.set_xticks([10, 100, 1000])
        ax.set_xlabel("radius /\u03BCm")

        ax.set_ylim([0, 1.8])
        ax.set_yticks([0, 0.4, 0.8, 1.2, 1.6])
        axes[1].set_ylabel("")

        ax.spines[["top", "right"]].set_visible(False)
    axes[2].set_xlim([3, 5000])
    axes[2].set_xticks([10, 100, 1000])
    axes[1].set_ylabel("mass density distribution, g(lnR) /g m$^{-3}$ / unit lnR")

    fig.tight_layout()

    return fig, axes
