"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: plot_compare_breakup.py
Project: collisions
Created Date: Wednesday 16th April 2025
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


import argparse
import sys
from pathlib import Path

# for imports from collisions src module
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))
import collisions.plot_compare_breakup as breakupplt


def main(path2CLEO, grid_filename, path2bin, path4figs, plot_marshall_parmer=False):
    if not plot_marshall_parmer:
        datasets = {}
        setups = {}
        for r in range(9):
            datasets[r] = path2bin / f"sol_bucomp_{r}.zarr"
            setups[r] = path2bin / f"setup_bucomp_{r}.txt"

        fig1, fig2, fig3 = breakupplt.plot_compare_breakup(
            path2CLEO, grid_filename, datasets, setups
        )

        savename = path4figs / "dejong2023_fig7a_as_timeseries.png"
        fig1.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w")
        print("Figure .png saved as: " + str(savename))

        savename = path4figs / "dejong2023_fig7a.pdf"
        fig2.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w")
        print("Figure .pdf saved as: " + str(savename))

        savename = path4figs / "dejong2023_fig8.png"
        fig3.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w")
        print("Figure .png saved as: " + str(savename))
    else:
        datasets = {}
        setups = {}
        for r in [2, 3, 4, 5]:
            datasets[r] = path2bin / f"sol_bucomp_marshpam_{r}.zarr"
            setups[r] = path2bin / f"setup_bucomp_marshpam_{r}.txt"

        fig4 = breakupplt.plot_compare_marshall_parmer_breakup(
            path2CLEO, grid_filename, datasets, setups
        )

        savename = path4figs / "dejong2023_fig9.pdf"
        fig4.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w")
        print("Figure .pdf saved as: " + str(savename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path2CLEO", type=Path, help="Absolute path of CLEO (for pySD)")
    parser.add_argument(
        "grid_filename", type=Path, help="Absolute path of .dat grid file"
    )
    parser.add_argument(
        "path2bin", type=Path, help="Absolute path to dataset and setup files"
    )
    parser.add_argument(
        "path4figs", type=Path, help="Absolute path for directory to save plots in"
    )
    args = parser.parse_args()

    plot_marshall_parmer = False

    main(
        args.path2CLEO,
        args.grid_filename,
        args.path2bin,
        args.path4figs,
        plot_marshall_parmer=plot_marshall_parmer,
    )
