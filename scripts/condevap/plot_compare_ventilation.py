"""
Copyright (c) 2026 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: plot_compare_ventilation.py
Project: condevap
Created Date: Thursday 1st January 1970
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


import argparse
import sys
from pathlib import Path

# for imports from condevap src module
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))
import condevap.plot_compare_ventilation as ventplt


def main(path2CLEO, grid_filename, path2bin_vent, path2bin_no_vent, path4figs):
    datasets = {}
    setups = {}
    n = 0
    for path2bin in [path2bin_vent, path2bin_no_vent]:
        for r in range(3):
            datasets[2 * r + n] = path2bin / f"sol_{r}.zarr"
            setups[2 * r + n] = path2bin / f"setup_{r}.txt"
        n += 1

    for r in range(6):
        print(datasets[r])

    fig1, fig2 = ventplt.quickplot(path2CLEO, grid_filename, datasets, setups)
    for f, fig in enumerate([fig1, fig2]):
        savename = path4figs / f"compare_ventilation_quickplot_{f}.png"
        fig.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w")
        print("Figure .png saved as: " + str(savename))

    fig, _ = ventplt.plot_compare_ventilation(
        path2CLEO, grid_filename, datasets, setups
    )
    savename = path4figs / "arabas_shima_2017_compare_ventilation.pdf"
    fig.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w")
    print("Figure .pdf saved as: " + str(savename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path2CLEO", type=Path, help="Absolute path of CLEO (for pySD)")
    parser.add_argument(
        "grid_filename", type=Path, help="Absolute path of .dat grid file"
    )
    parser.add_argument(
        "path2bin_vent",
        type=Path,
        help="Absolute path to dataset and setup files with ventilation factor",
    )
    parser.add_argument(
        "path2bin_no_vent",
        type=Path,
        help="Absolute path to dataset and setup files without ventilation factor",
    )
    parser.add_argument(
        "path4figs", type=Path, help="Absolute path for directory to save plots in"
    )
    args = parser.parse_args()

    main(
        args.path2CLEO,
        args.grid_filename,
        args.path2bin_vent,
        args.path2bin_no_vent,
        args.path4figs,
    )
