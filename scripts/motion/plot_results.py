"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: plot_results.py
Project: motion
Created Date: Thursday 24th April 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Saturday 2nd August 2025
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Source files to plot SD (as tracers) motion in flow similar to figure 1 of
Arabas et a. 2015 2-D model
"""


import argparse
import sys
from pathlib import Path

# for imports from motion src module
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))
import motion.plot_results as mtnplt


def main(path2CLEO, path2bin, path4figs):
    datasets = {}
    setups = {}
    for r in range(3):
        datasets[r] = path2bin / f"sol_{r}.zarr"
        setups[r] = path2bin / f"setup_{r}.txt"

    fig, axes = mtnplt.plot_results(path2CLEO, datasets, setups)
    savename = path4figs / "arabas_2015.png"
    fig.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w")
    print("Figure .png saved as: " + str(savename))

    fig, axes = mtnplt.plot_results_2(path2CLEO, datasets, setups)
    savename = path4figs / "arabas_2015_divergence_pergbx.png"
    fig.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w")
    print("Figure .png saved as: " + str(savename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path2CLEO", type=Path, help="Absolute path of CLEO (for pySD)")
    parser.add_argument(
        "path2bin", type=Path, help="Absolute path to dataset and setup files"
    )
    parser.add_argument(
        "path4figs", type=Path, help="Absolute path for directory to save plots in"
    )
    args = parser.parse_args()

    main(args.path2CLEO, args.path2bin, args.path4figs)
