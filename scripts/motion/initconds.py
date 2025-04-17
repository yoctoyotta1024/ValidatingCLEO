"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: initconds.py
Project: motion
Created Date: Thursday 17th April 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Thursday 17th April 2025
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Script generates input files for CLEO 2-D model similar to Arabas et al. 2015
E.g. execute
``
python ./scripts/motion/initconds.py ~/CLEO/ /work/bm1183/m300950/validating_cleo/build \
        /home/m/m300950/validating_cleo/src/motion/config.yaml False False
``
"""
import argparse
import sys
from pathlib import Path

# for imports from motion src module
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))
import motion.initconds as ic


def main(path2pySD, path2build, original_config, isfigures=[False, False]):
    if not (
        path2build.is_dir()
        and all([(path2build / f"{d}").is_dir() for d in ["tmp", "share", "bin"]])
    ):
        raise OSError(
            "Your build directory and bin, tmp, and share subdirectories do not exist"
        )
    else:
        for d in ["tmp", "share", "bin"]:
            path2dir = path2build / f"{d}" / "motion"
            path2dir.mkdir(exist_ok=True)

    config_filenames = ic.generate_configurations(
        path2pySD, path2build, original_config
    )

    ic.gridbox_boundaries(path2pySD, config_filenames[0], isfigures=isfigures)

    for cf in config_filenames:
        ic.initial_superdroplet_conditions(path2pySD, cf, isfigures=isfigures)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path2pySD", type=Path, help="Absolute path for CLEO (for pySD)"
    )
    parser.add_argument(
        "path2build", type=Path, help="Absolute path for build directory"
    )
    parser.add_argument(
        "original_config", type=Path, help="Absolute path for original config file"
    )
    parser.add_argument(
        "is_plotfigs",
        type=str,
        choices=["TRUE", "FALSE"],
        help="=='TRUE' then make initial condition figures",
    )
    parser.add_argument(
        "is_savefigs",
        type=str,
        choices=["TRUE", "FALSE"],
        help="=='TRUE' then save initial condition figures",
    )
    args = parser.parse_args()

    path2pySD = args.path2pySD
    path2build = args.path2build
    original_config = args.original_config
    isfigures = [False, False]
    if args.is_plotfigs == "TRUE":
        isfigures[0] = True
    if args.is_savefigs == "TRUE":
        isfigures[1] = True

    main(path2pySD, path2build, original_config, isfigures=isfigures)
