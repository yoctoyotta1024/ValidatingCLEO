"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: plot_results.py
Project: collisions
Created Date: Wednesday 16th April 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Tuesday 2nd September 2025
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
    path2pySD,
    ax,
    grid_filename,
    times2plot,
    datasets2plot,
    setups2plot,
    kernellabels,
    lwidths,
):
    import sys
    import awkward as ak
    import numpy as np
    import matplotlib.pyplot as plt

    sys.path.append(str(path2pySD))  # for imports from pySD package
    from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat, sdtracing

    ### time to plot: colour
    colors = {
        0: "midnightblue",
        600: "royalblue",
        1200: "darkviolet",
        1800: "tab:red",
        2400: "brown",
        3600: "sandybrown",
    }

    ### kernel: line [label, style]
    lstyles = {
        "Golovin 1963": [
            "Golovin",
            "-.",
        ],
        "Long 1974": [
            "hydro.",
            "-",
        ],
        "Testik 2011 + Straub 2010": [
            "incl. breakup",
            (0, (1, 1)),  # densely dotted
        ],
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
            tlab = "$t$ = {:.0f} s".format(time[ind])
            color = colors[t2plt]

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

            if n == 0:
                # to get black label with correct linestyle for legend
                fake_ax = plt.subplots()[1]
                kline = fake_ax.plot(
                    hcens,
                    hist,
                    color="k",
                    linestyle=lstyles[kernel][1],
                    linewidth=lwidths[nsupers],
                    zorder=0,
                )[0]
                khandles.append(kline)
                klab = f"{lstyles[kernel][0]}\n$N$={nsupers}"
                klabels.append(klab)

            ax.plot(
                hcens,
                hist,
                color=color,
                linestyle=lstyles[kernel][1],
                linewidth=lwidths[nsupers],
            )[0]
            tcolors.append(color)
            tlabels.append(tlab)

    y = 0.75
    for tlab, color in zip(tlabels, tcolors):
        ax.text(0.02, y, tlab, transform=ax.transAxes, color=color)
        y -= 0.055
    ax.legend(handles=khandles, labels=klabels, loc=(0.92, 0.5))

    return khandles, klabels


def plot_golovin_analytical(path2pySD, ax, times2plot, leg=None):
    import sys

    sys.path.append(
        str(path2pySD / "examples" / "exampleplotting")
    )  # imports from example plots package
    from plotssrc import shima2009fig

    rspan = [10, 1e4]
    nbins = 500
    n_a = 2**23
    r_a = 30.531e-06
    rho_l = 998.203
    for t in times2plot:
        golsol, hcens = shima2009fig.golovin_analytical(
            rspan,
            t,
            nbins,
            n_a,
            r_a,
            rho_l,
        )
        handles = ax.plot(hcens, golsol, color="grey", linestyle="-", linewidth=0.8)
    labels = ["Golovin\nanalytical"]
    if leg is not None:
        handles += leg[0]
        labels += leg[1]
    ax.legend(handles=handles, labels=labels, loc=(0.92, 0.5))


def plot_results(path2pySD, grid_filename, datasets, setups):
    import numpy as np
    import matplotlib.pyplot as plt

    ### nsupers: line width
    lwidths_1 = {
        8192: 0.8,
        131072: 2.0,
    }
    lwidths_2 = {
        131072: 0.8,
        2097152: 2.0,
    }

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(6.8, 11.5))

    ### plot golovin kernel datasets
    times2plot = [0, 1200, 2400, 3600]
    datasets2plot = [datasets[0], datasets[1]]
    setups2plot = [setups[0], setups[1]]
    kernellabels = ["Golovin 1963"] * 2
    khandles, klabels = plot_massdendistrib_evolution(
        path2pySD,
        axes[0],
        grid_filename,
        times2plot,
        datasets2plot,
        setups2plot,
        kernellabels,
        lwidths_1,
    )

    ### plot golovin kernel analytical solution
    plot_golovin_analytical(path2pySD, axes[0], times2plot, leg=[khandles, klabels])

    ### plot long and testikstraub datasets version 1
    times2plot = [0, 600, 1200, 1800]
    datasets2plot = [datasets[2], datasets[3], datasets[4], datasets[5]]
    setups2plot = [setups[2], setups[3], setups[4], setups[5]]
    kernellabels = ["Long 1974"] * 2 + ["Testik 2011 + Straub 2010"] * 2
    plot_massdendistrib_evolution(
        path2pySD,
        axes[1],
        grid_filename,
        times2plot,
        datasets2plot,
        setups2plot,
        kernellabels,
        lwidths_1,
    )

    ### plot long and testikstraub datasets version 2
    times2plot = [0, 1200, 2400, 3600]
    datasets2plot = [datasets[6], datasets[7], datasets[8], datasets[9]]
    setups2plot = [setups[6], setups[7], setups[8], setups[9]]
    kernellabels = ["Long 1974"] * 2 + ["Testik 2011 + Straub 2010"] * 2
    plot_massdendistrib_evolution(
        path2pySD,
        axes[2],
        grid_filename,
        times2plot,
        datasets2plot,
        setups2plot,
        kernellabels,
        lwidths_2,
    )

    ### beautify axes
    for ax in axes:
        ax.set_xscale("log")
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.spines[["top", "right"]].set_visible(False)

    for ax in [axes[0], axes[1]]:
        ax.set_xlim([10, 5000])
        ax.set_xticks([10, 100, 1000])

    for ax in [axes[1], axes[2]]:
        ax.set_ylim([0, 2.8])
        ax.set_yticks(np.arange(0.0, 2.8, 0.8))

    axes[0].set_ylim([0, 1.8])
    axes[0].set_yticks(np.arange(0.0, 1.8, 0.4))

    ylab = "mass density distribution / g m$^{-3}$ / $\u0394$ln($R$)"
    axes[1].set_ylabel(ylab)

    axes[2].set_xlim([3, 5000])
    axes[2].set_xticks([10, 100, 1000])
    axes[2].set_xlabel("R / \u03BCm")

    fig.tight_layout()

    return fig, axes
