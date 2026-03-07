"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: plot_compare_ventilation.py
Project: condevap
Created Date: Monday 14th April 2025
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
Script to plot middle row of figure 5 of S. Arabas and S. Shima 2017
using results from CLEO 0-D condensation/evaporation only box model
to compare effect of ventilation.
"""


def condensation_validation_subpplot(
    ax, time, radius, supersat, color, lwdth=1, lab="", lstyle="-"
):
    """adds the subplots of displacement, supersaturation
    and radial growth from Figure 5 of "On the CCN (de)activation
    nonlinearities" S. Arabas and S. Shima 2017"""

    l3 = ax.plot(
        radius,
        supersat,
        label=lab,
        color=color,
        linestyle=lstyle,
        linewidth=lwdth,
    )[0]

    return [l3]


def plot_one_dataset(
    path2pySD, ax, grid_filename, dataset, setupfile, color, vlab, lstyle
):
    ### imports
    import sys
    import numpy as np
    import random

    sys.path.append(str(path2pySD))  # for imports from pySD package
    sys.path.append(
        str(path2pySD / "examples" / "exampleplotting")
    )  # imports from example plots package

    from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat, sdtracing

    ### plot settings
    # w velocity [cm/s] : linewidth on plot
    lwdths = {
        1000.0: 1.25,
        500.0: 1,
        100.0: 0.75,
    }

    ### load data
    config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=True)
    consts = pysetuptxt.get_consts(setupfile, isprint=True)
    gbxs = pygbxsdat.get_gridboxes(grid_filename, consts["COORD0"], isprint=True)
    time = pyzarr.get_time(dataset).secs
    thermo = pyzarr.get_thermodata(dataset, config["ntime"], gbxs["ndims"], consts)
    supersat = thermo.relative_humidity() * 100  # thermo.supersaturation()

    sddata = pyzarr.get_supers(dataset, consts)
    sdid2plot = random.choice(sddata.sdId[0])  # plot one of the initial superdroplets
    attrs = ["radius", "xi", "msol"]
    sd2plot = sdtracing.attributes_for1superdroplet(sddata, sdid2plot, attrs)

    ### plot data
    w_avg = config["W_avg"] * 100
    lwdth = lwdths[w_avg]
    lines = condensation_validation_subpplot(
        ax,
        time,
        sd2plot["radius"],
        supersat[:, 0, 0, 0],
        color=color,
        lwdth=lwdth,
        lab=vlab,
        lstyle=lstyle,
    )

    volume = (
        gbxs["gbxvols"][0, 0, 0] * 1e6
    )  # assuming all gbxs have same volume [/cm^3]
    xi0 = np.where(
        sddata["sdgbxindex"][0] == 0, sddata["xi"][0], 0
    )  # 0th gbx's initial droplet xi
    numconc = np.sum(xi0) / volume  # initial number concentation in volume

    textlab = (
        r"r$_{\mathrm{w}}$ = "
        + "{:.2g} mm\n".format(sd2plot["radius"][0] / 1000)
        + r"$\mathrm{N}_{\mathrm{STP}}$ = "
        + str(numconc)
        + " cm$^{-3}$\n"
        + r"$w$ = {:.1f}".format(-1.0 * w_avg / 100)
        + " m s$^{-1}$"
    )
    ax.text(0.03, 0.85, textlab, transform=ax.transAxes, fontsize=12, color="k")

    return lines


def plot_compare_ventilation(path2pySD, grid_filename, datasets, setups):
    import matplotlib.pyplot as plt
    import numpy as np

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 5))

    vlab = [r"with $f_{\mathrm{v}}$", r"no $f_{\mathrm{v}}$"]
    color = ["tab:blue", "tab:green"]
    lstyle = ["-", "--"]

    for r in range(3):
        ax = axes[r]
        for i in range(2):
            dataset = datasets[2 * r + i]
            setupfile = setups[2 * r + i]
            plot_one_dataset(
                path2pySD,
                ax,
                grid_filename,
                dataset,
                setupfile,
                color=color[i],
                vlab=vlab[i],
                lstyle=lstyle[i],
            )

    axes[0].set_xscale("log")
    for ax in axes[1:]:
        xmin, xmax = ax.get_xlim()
        xticks = np.linspace(xmin, xmax, 4)
        ax.set_xticks(xticks)
        ax.set_xticklabels(["{:.0f}".format(x) for x in xticks])

    fsz = 12
    for ax in axes:
        ax.set_xlabel("$R$ /\u03BCm", fontsize=fsz)
        ax.spines[["right", "top"]].set_visible(False)
    axes[0].legend(fontsize=fsz)
    axes[0].set_ylabel("$RH$ /%", fontsize=fsz)

    fig.tight_layout()

    return fig, axes


def quickplot(path2CLEO, grid_filename, datasets, setups):
    import sys
    import matplotlib.pyplot as plt
    import xarray as xr

    sys.path.append(str(path2CLEO))  # for imports from pySD package
    from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat

    def displacement(time, w_avg, thalf):
        return 1000 - w_avg * time

    def relative_humidity(dataset, setupfile, grid_filename):
        config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=False)
        consts = pysetuptxt.get_consts(setupfile, isprint=False)
        gbxs = pygbxsdat.get_gridboxes(grid_filename, consts["COORD0"], isprint=False)
        thermo = pyzarr.get_thermodata(dataset, config["ntime"], gbxs["ndims"], consts)

        return thermo.relative_humidity()[:, 0, 0, 0] * 100  # percent

    label = ["vent", "no vent"]

    fig1, axes = plt.subplots(3, 5, figsize=(15, 10))
    for r in range(6):
        axs = axes[r // 2, :]
        ds = xr.open_dataset(datasets[r], engine="zarr")
        relh = relative_humidity(datasets[r], setups[r], grid_filename)

        axs[0].plot(ds.time, ds.temp, label=label[r % 2])
        axs[1].plot(ds.time, ds.press)
        axs[2].plot(ds.time, relh)
        axs[3].plot(ds.time, ds.radius / 1e3)
        axs[4].plot(ds.time, -ds.qcond)

    axes[0, 0].legend()
    axes[0, 0].set_title("Temperature / K")
    axes[0, 1].set_title("Pressure / hPa")
    axes[0, 2].set_title("Relative Humidity / %")
    axes[0, 3].set_title("Radius / mm")
    axes[0, 4].set_title(r"Cum. q$_{c}$ loss / g/kg")

    for ax in axes[-1, :]:
        ax.set_xlabel("time / s")
    fig1.tight_layout()

    fig2, axes = plt.subplots(3, 5, figsize=(15, 10))
    for r in range(6):
        axs = axes[r // 2, :]
        ds = xr.open_dataset(datasets[r], engine="zarr")
        config = pysetuptxt.get_config(setups[r], nattrs=3, isprint=True)
        zprof = displacement(ds.time.values, config["W_avg"], config["TAU_half"])
        relh = relative_humidity(datasets[r], setups[r], grid_filename)

        axs[0].plot(ds.temp, zprof, label=label[r % 2])
        axs[1].plot(ds.press, zprof)
        axs[2].plot(relh, zprof)
        axs[3].plot(ds.radius / 1e3, zprof)
        axs[4].plot(-ds.qcond, zprof)

    axes[0, 0].set_title("Temperature / K")
    axes[0, 1].set_title("Pressure / hPa")
    axes[0, 2].set_title("Relative Humidity / %")
    axes[0, 3].set_title("Radius / mm")
    axes[0, 4].set_title(r"Cum. q$_{c}$ loss / g/kg")

    for ax in axes[:, 0]:
        ax.set_ylabel("height / m")

    axes[0, 0].legend()
    fig2.tight_layout()

    return fig1, fig2
