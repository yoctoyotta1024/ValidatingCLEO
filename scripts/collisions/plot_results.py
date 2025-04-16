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
Script to plot figure 2 of Shima et al. 2009 using results from CLEO
0-D collisions-only box model.
"""


import argparse
import sys
from pathlib import Path

# for imports from collisions src module
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))
import collisions.plot_results as collsplt


def main(path2CLEO, grid_filename, path2bin, path4figs):
    datasets = {}
    setups = {}
    for r in range(10):
        datasets[r] = path2bin / f"sol_{r}.zarr"
        setups[r] = path2bin / f"setup_{r}.txt"

    fig, axes = collsplt.plot_results(path2CLEO, grid_filename, datasets, setups)
    savename = path4figs / "shima_2009.png"
    fig.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w")
    print("Figure .png saved as: " + str(savename))


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

    path2CLEO = args.path2CLEO
    grid_filename = args.grid_filename
    path2bin = args.path2bin
    path4figs = args.path4figs

    main(args.path2CLEO, args.grid_filename, args.path2bin, args.path4figs)
