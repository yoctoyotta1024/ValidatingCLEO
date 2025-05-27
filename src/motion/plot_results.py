"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: plot_results.py
Project: motion
Created Date: Thursday 24th April 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Friday 25th April 2025
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


def plot_superdroplet_sample_2dmotion(fig, ax, time, sdsample, cax=None):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.cm import ScalarMappable

    cmap = "YlGnBu"  # for superdroplet radii
    cmap_norm = plt.Normalize(vmin=0, vmax=60)
    c = np.repeat(time.mins, (sdsample["coord3"].shape)[1])

    if cax is not None:
        fig.colorbar(
            ScalarMappable(norm=cmap_norm, cmap=cmap),
            cax=cax,
            label="time /mins",
            orientation="horizontal",
        )

    ax.scatter(
        sdsample["coord1"],
        sdsample["coord3"],
        c=c,
        cmap=cmap,
        norm=cmap_norm,
        marker=".",
        s=0.001,
    )
    ax.set_aspect("equal")
    ax.set_xlabel("$x$ / m")
    ax.set_ylabel("$z$ / m")
    ax.set_xlim([0, 1500])
    ax.set_ylim([0, 1500])
    ax.set_xticks([0, 750, 1500])
    ax.set_yticks([0, 750, 1500])
    ax.spines[["left", "right"]].set_visible(False)


def plot_results(path2pySD, datasets, setups):
    import sys
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    sys.path.append(str(path2pySD))
    from pySD.sdmout_src import pyzarr, pysetuptxt

    fig = plt.figure(figsize=(4, 10.5))  # (3, 8) fits well
    gs = GridSpec(4, 1, figure=fig, height_ratios=[1] + [23] * 3)
    cax = fig.add_subplot(gs[0, :])

    axes = [cax]
    resolutions = [100, 50, 25]
    for r in range(3):
        ax = fig.add_subplot(gs[r + 1, :])
        dataset = datasets[r]
        setupfile = setups[r]
        res = resolutions[r]

        ### read in constants and intial setup from setup .txt file
        consts = pysetuptxt.get_consts(setupfile, isprint=True)

        # read in output Xarray data
        time = pyzarr.get_time(dataset)
        sddata = pyzarr.get_supers(dataset, consts)

        nsample = 500
        attrs4sample = ["coord1", "coord3"]
        times2plot = time.mins
        sdsample = random_sample_superdroplet_data(
            sddata, nsample, attrs4sample, times2plot
        )

        plot_superdroplet_sample_2dmotion(fig, ax, time, sdsample, cax=cax)
        t = ax.text(
            1500, 1350, f"$\u0394 x = \u0394 z = {res}$ m", color="k", ha="right"
        )
        t.set_bbox(dict(facecolor="w", alpha=0.75, linewidth=0))
        axes.append(ax)
        cax = None  # only plot cax once

    fig.tight_layout()

    return fig, axes
