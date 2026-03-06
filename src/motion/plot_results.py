"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: plot_results.py
Project: motion
Created Date: Thursday 24th April 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Friday 6th March 2026
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Source files to plot SD (as tracers) motion in flow similar to figure 1 of
Arabas et a. 2015 2-D model
"""


def random_sample_superdroplet_data(sddata, nsample, attrs, times2select):
    """function copied from ```prettyplots_thermo3d.py``` file in github
    repository ```yoctoyotta1024/PerformanceTestingCLEO v2.5.1```"""
    import numpy as np
    import awkward as ak

    sdId = sddata["sdId"]
    sds2sample = np.random.choice(sdId[0], size=nsample, replace=False)

    data_sample = {}
    for attr in attrs:
        data_sample[attr] = []

    for t in range(len(times2select)):
        sdid_sample, idxs, _ = np.intersect1d(
            sdId[t], sds2sample, assume_unique=True, return_indices=True
        )
        idxs = ak.to_numpy(idxs).astype("int32")

        tsample = {}
        for attr in attrs:
            tsample[attr] = sddata[attr][t][idxs]

        if len(sdid_sample) != nsample:
            missing_sds = np.setdiff1d(sds2sample, sdid_sample, assume_unique=True)
            missing_idxs = np.searchsorted(sdid_sample, missing_sds)
            for attr in attrs:
                tsample[attr] = np.insert(tsample[attr], missing_idxs, np.nan)

        for attr in attrs:
            data_sample[attr].append(tsample[attr])

    for attr in attrs:
        data_sample[attr] = np.asarray(data_sample[attr])

    return data_sample


def sample_for_motion_plot(path2pySD, dataset, consts):
    import sys

    sys.path.append(str(path2pySD))
    from pySD.sdmout_src import pyzarr

    # read in output Xarray data
    time = pyzarr.get_time(dataset)
    sddata = pyzarr.get_supers(dataset, consts)

    nsample = 500
    attrs4sample = ["coord1", "coord3"]
    times2plot = time.mins
    sdsample = random_sample_superdroplet_data(
        sddata, nsample, attrs4sample, times2plot
    )

    return time, sdsample


def plot_superdroplet_sample_2dmotion(fig, ax, time, sdsample, cax=None, topcbar=False):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.cm import ScalarMappable

    cmap = "YlGnBu"  # for superdroplet radii
    cmap_norm = plt.Normalize(vmin=0, vmax=60)
    c = np.repeat(time.mins, (sdsample["coord3"].shape)[1])

    if cax is not None:
        cbar = fig.colorbar(
            ScalarMappable(norm=cmap_norm, cmap=cmap),
            cax=cax,
            label="time /mins",
            orientation="horizontal",
        )
        if topcbar:
            cbar.ax.xaxis.set_ticks_position("top")
            cbar.ax.xaxis.set_label_position("top")

    ax.scatter(
        sdsample["coord1"],
        sdsample["coord3"],
        c=c,
        cmap=cmap,
        norm=cmap_norm,
        marker=".",
        s=0.001,
    )


def plot_divergence_pergbx(ax, ds):
    time = ds.time.values

    ax.plot(time, ds.nsupers.values, alpha=0.3, linewidth=0.5, zorder=0)

    mean = ds.nsupers.mean(dim="gbxindex")
    std = ds.nsupers.std(dim="gbxindex")
    ax.plot(time, mean, color="k", linewidth=1.0, zorder=2)
    ax.plot(time, mean + std, color="k", linestyle="dashed", linewidth=1.0, zorder=2)
    ax.plot(time, mean - std, color="k", linestyle="dashed", linewidth=1.0, zorder=2)

    return ax


def plot_motion_figure(path2pySD, datasets, setups):
    import sys
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    sys.path.append(str(path2pySD))
    from pySD.sdmout_src import pysetuptxt

    fig = plt.figure(figsize=(4, 10.5))  # (3, 8) fits well
    gs = GridSpec(4, 1, figure=fig, height_ratios=[1] + [23] * 3)
    cax = fig.add_subplot(gs[0, :])
    axes = []
    for r in range(3):
        ax = fig.add_subplot(gs[r + 1, :])
        axes.append(ax)
    axes.append(cax)

    for r in range(3):
        ax = axes[r]
        dataset = datasets[r]
        setupfile = setups[r]

        consts = pysetuptxt.get_consts(setupfile, isprint=True)
        time, sdsample = sample_for_motion_plot(path2pySD, dataset, consts)
        plot_superdroplet_sample_2dmotion(fig, ax, time, sdsample, cax=cax)
        cax = None  # only plot cax once

    resolutions = [100, 50, 25]
    for r in range(3):
        ax = axes[r]
        res = resolutions[r]
        ax.set_aspect("equal")
        ax.set_xlabel("$x$ / m")
        ax.set_ylabel("$z$ / m")
        ax.set_xlim([0, 1500])
        ax.set_ylim([0, 1500])
        ax.set_xticks([0, 750, 1500])
        ax.set_yticks([0, 750, 1500])
        ax.spines[["left", "right"]].set_visible(False)
        t = ax.text(
            1500, 1350, f"$\u0394 x = \u0394 z = {res}$ m", color="k", ha="right"
        )
        t.set_bbox(dict(facecolor="w", alpha=0.75, linewidth=0))

    fig.tight_layout()

    return fig, axes


def plot_divergence_pergbx_figure(datasets):
    import xarray as xr
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(nrows=len(datasets), ncols=1, figsize=(5, 9))

    for r in range(3):
        ax = axes[r]
        ds = xr.open_dataset(datasets[r], engine="zarr")
        plot_divergence_pergbx(ax, ds)

    resolutions = [100, 50, 25]
    for r in range(3):
        ax = axes[r]
        res = resolutions[r]
        ax.set_xlim(0, 3600)
        ax.set_ylim(50, 200)
        ax.spines[["right", "top"]].set_visible(False)
        ax.set_xlabel("time / s")
        ax.set_ylabel("superdroplets per grid-box")
        t = ax.text(
            3500, 180, f"$\u0394 x = \u0394 z = {res}$ m", color="k", ha="right"
        )
        t.set_bbox(dict(facecolor="w", alpha=0.75, linewidth=0))

    fig.tight_layout()

    return fig, axes


def plot_motion_and_divergence_figure(path2pySD, datasets, setups):
    import sys
    import matplotlib.pyplot as plt
    import xarray as xr
    from matplotlib.gridspec import GridSpec

    sys.path.append(str(path2pySD))
    from pySD.sdmout_src import pysetuptxt

    fig = plt.figure(figsize=(10, 5))  # (3, 8) fits well
    gs = GridSpec(
        4,
        5,
        figure=fig,
        width_ratios=[7, 1, 7, 1, 7],
        height_ratios=[1, 23, 1, 12],
        hspace=0.5,
    )
    cax = fig.add_subplot(gs[0, 1:4])

    axes1 = []
    for r in range(3):
        ax = fig.add_subplot(gs[1, 2 * r])
        axes1.append(ax)
    axes1.append(cax)

    axes2 = []
    for r in range(3):
        ax = fig.add_subplot(gs[3, 2 * r])
        axes2.append(ax)
    axes2.append(cax)

    for r in range(3):
        dataset = datasets[r]
        setupfile = setups[r]
        ds = xr.open_dataset(dataset, engine="zarr")
        consts = pysetuptxt.get_consts(setupfile, isprint=True)

        time, sdsample = sample_for_motion_plot(path2pySD, dataset, consts)
        plot_superdroplet_sample_2dmotion(
            fig, axes1[r], time, sdsample, cax=cax, topcbar=True
        )
        cax = None  # only plot cax once

        plot_divergence_pergbx(axes2[r], ds)

    resolutions = [100, 50, 25]
    for r in range(3):
        ax = axes1[r]
        res = resolutions[r]
        ax.set_aspect("equal")
        ax.set_xlabel("$x$ / m")
        ax.set_ylabel("$z$ / m")
        ax.set_xlim([0, 1500])
        ax.set_ylim([0, 1500])
        ax.set_xticks([0, 750, 1500])
        ax.set_yticks([0, 750, 1500])
        ax.spines[["left", "right"]].set_visible(False)
        ax.set_title(f"$\u0394 x = \u0394 z = {res}$ m")

    for r in range(3):
        ax = axes2[r]
        res = resolutions[r]
        ax.set_xlim(0, 3600)
        ax.set_ylim(50, 200)
        ax.spines[["right", "top"]].set_visible(False)
        ax.set_xlabel("time / s")
        ax.set_ylabel("$n_{\mathrm{s}}$")

    return fig, [axes1, axes2]


def plot_results(path2pySD, datasets, setups):
    fig1, _ = plot_motion_and_divergence_figure(path2pySD, datasets, setups)

    fig2, _ = plot_motion_figure(path2pySD, datasets, setups)

    fig3, _ = plot_divergence_pergbx_figure(datasets)

    return fig1, fig2, fig3
