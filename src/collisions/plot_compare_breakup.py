"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: plot_compare_breakup.py
Project: collisions
Created Date: Monday 9th March 2026
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Monday 9th March 2026
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Script to plot Figures from de Jong et al. 2023 to compare breakup methods
using results from CLEO 0-D collisions-only box model.
"""


def calc_massdendistrib(
    path2pySD, sddata2plot, time_n, gbxs, sddata, nbins, rspan, smoothsig
):
    import sys
    import numpy as np

    sys.path.append(
        str(path2pySD / "examples" / "exampleplotting")
    )  # imports from example plots package
    from plotssrc import shima2009fig

    sdgbxindex = sddata2plot["sdgbxindex"][time_n]
    radius = sddata2plot["radius"][time_n]
    xi = sddata2plot["xi"][time_n]
    nsupers = len(sdgbxindex)

    mass = np.sum(1000.0 * 4.0 / 3.0 * (radius / 1e6) ** 3 * np.pi * xi) * 1000 / 1e6
    print(f"mass of water in domain = {mass} g cm-3")

    gbx2plt = 0  # plot 0th gridbox
    volume = gbxs["gbxvols"][0, 0, 0]  # assuming all gbxs have same volume [m^3]

    radius = np.where(sdgbxindex == gbx2plt, radius, np.nan)
    xi = np.where(sdgbxindex == gbx2plt, xi, np.nan)

    hist, hcens = shima2009fig.calc_massdens_distrib(
        rspan, nbins, volume, xi, radius, sddata, smoothsig
    )

    return hist, hcens, nsupers


def calc_numconcdistrib(sddata2plot, time_n, gbxs, nbins, rspan):
    import numpy as np

    sdgbxindex = sddata2plot["sdgbxindex"][time_n]
    radius = sddata2plot["radius"][time_n] / 1e6  # [m]
    xi = sddata2plot["xi"][time_n]

    gbx2plt = 0  # plot 0th gridbox
    volume = gbxs["gbxvols"][0, 0, 0]  # assuming all gbxs have same volume [m^3]

    radius = np.where(sdgbxindex == gbx2plt, radius, np.nan)
    xi = np.where(sdgbxindex == gbx2plt, xi, np.nan)

    wghts = xi / volume  # real droplets [m^-3]
    hedgs = np.linspace(rspan[0], rspan[1], nbins)  # [m]
    hist, hedgs = np.histogram(radius, bins=hedgs, weights=wghts)
    hwdths = hedgs[1:] - hedgs[:-1]
    hcens = hedgs[:-1] + hwdths / 2

    return hist, hedgs, hcens, hwdths


def plot_step_dist_on_axes(ax, hcens, hist, kwargs):
    return ax.step(hcens, hist, where="mid", **kwargs)[0]


def plot_massdendistrib_evolution_timeseries(
    path2pySD,
    ax,
    grid_filename,
    times2plot,
    datasets2plot,
    setups2plot,
    lwidths,
    lstyles,
    colors,
    is_legend=False,
    is_text=False,
    is_title=False,
):
    import sys
    import numpy as np
    import matplotlib.pyplot as plt

    sys.path.append(str(path2pySD))  # for imports from pySD package
    from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat, sdtracing

    khandles, klabels = [], []
    for key, dataset in datasets2plot.items():
        setupfile = setups2plot[key]
        ### read in constants and intial setup from setup .txt file
        config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=True)
        consts = pysetuptxt.get_consts(setupfile, isprint=True)
        gbxs = pygbxsdat.get_gridboxes(grid_filename, consts["COORD0"], isprint=True)

        # read in output Xarray data
        time = pyzarr.get_time(dataset).secs
        sddata = pyzarr.get_supers(dataset, consts)

        smoothsig = False
        rspan = [1, 1e4]
        nbins = 128

        attrs2sel = ["sdgbxindex", "radius", "xi"]
        sddata2plot = sdtracing.attributes_at_times(sddata, time, times2plot, attrs2sel)

        tcolors, tlabels = [], []
        for n, t2plt in enumerate(times2plot):
            ind = np.argmin(abs(time - t2plt))
            tlab = "$t$ = {:.0f} s".format(time[ind])

            hist, hcens, nsupers = calc_massdendistrib(
                path2pySD, sddata2plot, n, gbxs, sddata, nbins, rspan, smoothsig
            )
            hist = hist / 1000  # g/m^3 -> kg/m^3

            if n == 0:
                # to get black label with correct linestyle for legend
                fake_ax = plt.subplots()[1]
                leg_kwargs = {  # should match kwargs below except for colour
                    "color": "k",
                    "linestyle": lstyles[key][1],
                    "linewidth": lwidths[nsupers],
                    "zorder": 0,
                }
                kline = plot_step_dist_on_axes(fake_ax, hcens, hist, leg_kwargs)
                khandles.append(kline)

                klab = lstyles[key][0]
                nfrags = config["nfrags"]
                if nfrags > 0.0:
                    klab = klab + "=" + f"{nfrags}"
                klabels.append(klab)

            kwargs = {
                "color": colors[t2plt],
                "linestyle": lstyles[key][1],
                "linewidth": lwidths[nsupers],
                "zorder": 0,
            }
            plot_step_dist_on_axes(ax, hcens, hist, kwargs)

            tcolors.append(colors[t2plt])
            tlabels.append(tlab)

    if is_text:
        y = 0.85
        for tlab, color in zip(tlabels, tcolors):
            ax.text(0.03, y, tlab, transform=ax.transAxes, color=color, fontsize=11)
            y -= 0.08
    if is_legend:
        ax.legend(handles=khandles, labels=klabels, loc=(0.92, 0.5))
    if is_title:
        ax.set_title(klabels[0])

    return khandles, klabels


def plot_massdendistrib_evolution_oneplot(
    path2pySD,
    ax,
    grid_filename,
    times2plot,
    datasets2plot,
    setups2plot,
    lwidths,
    lstyles,
    labels_colors,
    is_legend=False,
    is_title=False,
    is_plot_t0=True,
):
    import sys
    import numpy as np

    sys.path.append(str(path2pySD))  # for imports from pySD package
    from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat, sdtracing

    khandles, klabels = [], []
    for key, dataset in datasets2plot.items():
        setupfile = setups2plot[key]
        ### read in constants and intial setup from setup .txt file
        config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=True)
        consts = pysetuptxt.get_consts(setupfile, isprint=True)
        gbxs = pygbxsdat.get_gridboxes(grid_filename, consts["COORD0"], isprint=True)

        # read in output Xarray data
        time = pyzarr.get_time(dataset).secs
        sddata = pyzarr.get_supers(dataset, consts)

        smoothsig = False
        rspan = [1, 1e4]
        nbins = 64

        attrs2sel = ["sdgbxindex", "radius", "xi"]
        sddata2plot = sdtracing.attributes_at_times(sddata, time, times2plot, attrs2sel)

        for n, t2plt in enumerate(times2plot):
            ind = np.argmin(abs(time - t2plt))
            print("plotting on Fig. 7a at t = ", time[ind])

            hist, hcens, nsupers = calc_massdendistrib(
                path2pySD, sddata2plot, n, gbxs, sddata, nbins, rspan, smoothsig
            )
            hist = hist / 1000  # g/m^3 -> kg/m^3

            if t2plt == 0:
                label = "t=0s"
                color = "k"
            else:
                label = labels_colors[key][0]
                nfrags = config["nfrags"]
                if nfrags > 0.0:
                    label = label + "=" + f"{nfrags}"
                color = labels_colors[key][1]

            kwargs = {
                "color": color,
                "linestyle": lstyles[t2plt],
                "linewidth": lwidths[nsupers],
                "zorder": 0,
                "label": label,  # only label first time to avoid duplicates in legend
            }
            if (is_plot_t0 and t2plt == 0) or t2plt != 0:
                plot_step_dist_on_axes(ax, hcens, hist, kwargs)

    if is_legend:
        ax.legend(handles=khandles, labels=klabels)
    if is_title:
        ax.set_title(klabels[0])

    return khandles, klabels


def plot_dejong_figure8(path2pySD, grid_filename, datasets2plot, setups2plot):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(10, 6))  # (3, 8) fits well
    gs = GridSpec(2, 6, figure=fig)
    axes = [
        fig.add_subplot(gs[0, :3]),
        fig.add_subplot(gs[0, 3:]),
        fig.add_subplot(gs[1, :2]),
        fig.add_subplot(gs[1, 2:4]),
        fig.add_subplot(gs[1, 4:]),
    ]

    times2plot = [0, 60, 240, 1800, 7200]

    ### nsupers: line width
    lwidths = {
        8192: 0.8,
    }

    ### time to plot: colour
    colors = {
        0: "black",
        60: "navy",
        240: "teal",
        1800: "darkturquoise",
        7200: "springgreen",
    }

    ### dataset_key: line [label, style]
    lstyles = {
        "testikstraub": [
            "T2009+Str2010 & Sch2010",
            (0, (1, 1)),
        ],  # densely dotted
        "schlottke": ["Str2010 & Sch2010", "-"],
        "nfrags_0": [
            r"Str2010 & $\mathrm{N}_{\mathrm{frag}}$",
            "--",
        ],
        "nfrags_1": [
            r"Str2010 & $\mathrm{N}_{\mathrm{frag}}$",
            "--",
        ],
        "nfrags_2": [
            r"Str2010 & $\mathrm{N}_{\mathrm{frag}}$",
            "--",
        ],
    }

    for i, key in enumerate(datasets2plot.keys()):
        plot_massdendistrib_evolution_timeseries(
            path2pySD,
            axes[i],
            grid_filename,
            times2plot,
            {key: datasets2plot[key]},
            {key: setups2plot[key]},
            lwidths,
            lstyles,
            colors,
            is_title=True,
            is_text=True if i == 0 else False,
        )

    ### beautify axes
    for ax in axes:
        ax.set_xscale("log")
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.spines[["top", "right"]].set_visible(False)

    for ax in axes:
        ax.set_xlim([1, 1e4])

    for ax in axes[1:]:
        ax.set_ylim([0, 0.035])
        yticks = np.arange(0.0, 0.04, 0.005)
        ax.set_yticks(yticks)
    axes[0].set_ylim([0, 0.1025])

    ylab = "mass density distribution\n/ kg m$^{-3}$ / $\u0394$ln($R$)"
    for ax in [axes[0], axes[2]]:
        ax.set_ylabel(ylab)
    for ax in [axes[2], axes[3], axes[4]]:
        ax.set_xlabel("R / \u03BCm")

    fig.tight_layout()

    return fig, axes


def plot_dejong_figure7a_as_timeseries(
    path2pySD, grid_filename, datasets2plot, setups2plot
):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(10, 6))  # (3, 8) fits well
    gs = GridSpec(2, 2, figure=fig)
    axes = [
        fig.add_subplot(gs[0, :1]),
        fig.add_subplot(gs[0, 1:]),
        fig.add_subplot(gs[1, :1]),
        fig.add_subplot(gs[1, 1:]),
    ]

    times2plot = [0, 10, 20, 30, 60, 120]

    ### nsupers: line width
    lwidths = {
        8192: 0.8,
    }

    ### time to plot: colour
    colors = {
        0: "black",
        10: "blue",
        20: "green",
        30: "yellow",
        60: "orange",
        120: "red",
    }

    ### dataset_key: line [label, style]
    lstyles = {
        "coal": [
            "Coalescence Only",
            "-",
        ],  # densely dotted
        "nfrags_0": [
            r"$\mathrm{N}_{\mathrm{frag}}$",
            "--",
        ],
        "nfrags_1": [
            r"$\mathrm{N}_{\mathrm{frag}}$",
            "--",
        ],
        "nfrags_2": [
            r"$\mathrm{N}_{\mathrm{frag}}$",
            "--",
        ],
    }

    for i, key in enumerate(datasets2plot.keys()):
        plot_massdendistrib_evolution_timeseries(
            path2pySD,
            axes[i],
            grid_filename,
            times2plot,
            {key: datasets2plot[key]},
            {key: setups2plot[key]},
            lwidths,
            lstyles,
            colors,
            is_title=True,
            is_text=True if i == 0 else False,
        )

    ### beautify axes
    for ax in axes:
        ax.set_xscale("log")
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.spines[["top", "right"]].set_visible(False)

    for ax in axes:
        ax.set_xlim([1, 1e4])
        ax.set_ylim([0, 0.035])
        yticks = np.arange(0.0, 0.04, 0.005)
        ax.set_yticks(yticks)

    ylab = "mass density distribution\n/ kg m$^{-3}$ / $\u0394$ln($R$)"
    for ax in [axes[0], axes[2]]:
        ax.set_ylabel(ylab)
    for ax in [axes[2], axes[3]]:
        ax.set_xlabel("R / \u03BCm")

    fig.tight_layout()

    return fig, axes


def plot_dejong_figure7a(path2pySD, grid_filename, datasets2plot, setups2plot):
    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    axes = [ax]

    times2plot = [0, 120]

    ### nsupers: line width
    lwidths = {
        8192: 0.8,
    }

    ### nfrags: [label, colour]
    labels_colors = {
        "coal": ["Coalescence Only", "purple"],
        "nfrags_0": ["$\mathrm{N}_{\mathrm{frag}}$", "blue"],
        "nfrags_1": ["$\mathrm{N}_{\mathrm{frag}}$", "turquoise"],
        "nfrags_2": ["$\mathrm{N}_{\mathrm{frag}}$", "green"],
    }

    ### time_to_plot: linestyle
    lstyles = {
        0: "--",
        120: "-",
    }

    is_plot_t0 = True
    for i, key in enumerate(datasets2plot.keys()):
        plot_massdendistrib_evolution_oneplot(
            path2pySD,
            axes[0],
            grid_filename,
            times2plot,
            {key: datasets2plot[key]},
            {key: setups2plot[key]},
            lwidths,
            lstyles,
            labels_colors,
            is_legend=True,
            is_plot_t0=is_plot_t0,
        )
        is_plot_t0 = False  # only plot initial conditions once

    ### beautify axes
    for ax in axes:
        ax.set_xscale("log")
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.spines[["top", "right"]].set_visible(False)

    for ax in axes:
        ax.set_xlim([1, 1e4])
        ax.set_ylim([0, 0.035])
        yticks = np.arange(0.0, 0.04, 0.005)
        ax.set_yticks(yticks)

    ylab = "mass density distribution\n/ kg m$^{-3}$ / $\u0394$ln($R$)"
    axes[0].set_ylabel(ylab)
    axes[0].set_xlabel("R / \u03BCm")

    fig.tight_layout()

    return fig, axes


def plot_compare_breakup(path2pySD, grid_filename, datasets, setups):
    # constant coaleff with different constant nfrags
    datasets2plot = {
        "coal": datasets[0],
        "nfrags_0": datasets[6],
        "nfrags_1": datasets[7],
        "nfrags_2": datasets[8],
    }
    setups2plot = {
        "coal": setups[0],
        "nfrags_0": setups[6],
        "nfrags_1": setups[7],
        "nfrags_2": setups[8],
    }
    fig1, _ = plot_dejong_figure7a_as_timeseries(
        path2pySD, grid_filename, datasets2plot, setups2plot
    )
    fig2, _ = plot_dejong_figure7a(path2pySD, grid_filename, datasets2plot, setups2plot)

    # testik straub or straub coaleff with different nfrag formulas
    datasets2plot = {
        "testikstraub": datasets[1],
        "schlottke": datasets[2],
        "nfrags_0": datasets[3],
        "nfrags_1": datasets[4],
        "nfrags_2": datasets[5],
    }
    setups2plot = {
        "testikstraub": setups[1],
        "schlottke": setups[2],
        "nfrags_0": setups[3],
        "nfrags_1": setups[4],
        "nfrags_2": setups[5],
    }
    fig3, _ = plot_dejong_figure8(path2pySD, grid_filename, datasets2plot, setups2plot)

    return fig1, fig2, fig3


def plot_numconc_normalised_distribs(
    path2pySD, ax, times2plot, grid_filename, dataset, setupfile, kwargs
):
    import sys
    import numpy as np

    sys.path.append(str(path2pySD))  # for imports from pySD package
    from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat, sdtracing

    ### read in constants and intial setup from setup .txt file
    config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=True)
    consts = pysetuptxt.get_consts(setupfile, isprint=True)
    gbxs = pygbxsdat.get_gridboxes(grid_filename, consts["COORD0"], isprint=True)

    # read in output Xarray data
    time = pyzarr.get_time(dataset).secs
    sddata = pyzarr.get_supers(dataset, consts)

    rspan = [0, 7e-3]
    nbins = 128

    attrs2sel = ["sdgbxindex", "radius", "xi"]
    sddata2plot = sdtracing.attributes_at_times(sddata, time, times2plot, attrs2sel)

    for n, t2plt in enumerate(times2plot):
        ind = np.argmin(abs(time - t2plt))
        print("plotting at t = ", time[ind])

        hist, hedgs, hcens, hwdths = calc_numconcdistrib(
            sddata2plot, n, gbxs, nbins, rspan
        )
        hist_normalised = hist / hwdths / 1000  # num conc per bin / m^-3 mm^-1
        hcens = hcens * 2e3  # convert radius to diam [mm]

        nfrags = config["nfrags"]
        if nfrags > 0.0:
            kwargs["label"] = kwargs["label"] + "=" + f"{nfrags}"

        plot_step_dist_on_axes(ax, hcens, hist_normalised, kwargs)
    ax.set_yscale("log")

    return ax


def plot_straub_fig10_data(ax):
    from .straub2010_data import get_straub_fig10_data

    x, y = get_straub_fig10_data()
    ax.plot(x, y, color="k", linestyle="--")
    return ax


def plot_dejong_figure9(path2pySD, grid_filename, datasets2plot, setups2plot):
    import matplotlib.pyplot as plt

    ### nfrags: [label, colour]
    labels_colors_lstyles = {
        "schlottke": ["Schlottke et al. 2010", "orangered", "solid"],
        "nfrags_0": ["$\mathrm{N}_{\mathrm{frag}}$", "blue", "dashdot"],
        "nfrags_1": ["$\mathrm{N}_{\mathrm{frag}}$", "dodgerblue", "dashdot"],
        "nfrags_2": ["$\mathrm{N}_{\mathrm{frag}}$", "fuchsia", "dashdot"],
    }

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))

    times2plot = [0]
    for key, dataset in datasets2plot.items():
        kwargs = {
            "color": "k",
            "label": labels_colors_lstyles[key][0],
            "linestyle": labels_colors_lstyles[key][2],
        }
        plot_numconc_normalised_distribs(
            path2pySD,
            axes[0],
            times2plot,
            grid_filename,
            dataset,
            setups2plot[key],
            kwargs,
        )

    times2plot = [7200]
    for key, dataset in datasets2plot.items():
        kwargs = {
            "label": labels_colors_lstyles[key][0],
            "color": labels_colors_lstyles[key][1],
            "linestyle": labels_colors_lstyles[key][2],
        }
        plot_numconc_normalised_distribs(
            path2pySD,
            axes[1],
            times2plot,
            grid_filename,
            dataset,
            setups2plot[key],
            kwargs,
        )

    plot_straub_fig10_data(axes[1])

    for ax in axes:
        ax.set_xlim([0, 4])
        ax.set_ylim([10, 2e5])
        ax.set_xlabel("diameter / mm")
        ax.set_ylabel("number concentration / m$^{-3}$ mm$^{-1}$")
        ax.spines[["top", "right"]].set_visible(False)

    axes[1].legend(loc=(-1.1, 0.6))

    fig.subplots_adjust(wspace=0.4)

    return fig, axes


def plot_compare_marshall_parmer_breakup(path2pySD, grid_filename, datasets, setups):
    # straub coaleff with different nfrags
    datasets2plot = {
        "schlottke": datasets[2],
        "nfrags_0": datasets[3],
        "nfrags_1": datasets[4],
        "nfrags_2": datasets[5],
    }
    setups2plot = {
        "schlottke": setups[2],
        "nfrags_0": setups[3],
        "nfrags_1": setups[4],
        "nfrags_2": setups[5],
    }
    fig4, _ = plot_dejong_figure9(path2pySD, grid_filename, datasets2plot, setups2plot)

    return fig4
