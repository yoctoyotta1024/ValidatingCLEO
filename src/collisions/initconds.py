"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: initconds.py
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
Source files for script to generates input files for CLEO 0-D box model with
droplet size distribution as in Shima et al. 2009.
"""


def generate_configurations(path2pySD, path2build, original_config):
    import shutil
    import sys

    sys.path.append(str(path2pySD))  # for imports from pySD package
    from pySD import editconfigfile

    # parameters same for each run
    tmppath = path2build / "tmp" / "collisions"
    sharepath = path2build / "share" / "collisions"
    binpath = path2build / "bin" / "collisions"
    savefigpath = binpath
    constants_filename = (
        path2build / "_deps" / "cleo-src" / "libs" / "cleoconstants.hpp"
    )
    grid_filename = sharepath / "dimlessGBxboundaries.dat"

    # parameters specific for each run
    nruns = 10
    volexpr0 = [30.531e-06] * 6 + [10.177e-06] * 4
    numconc = [2**23] * 6 + [3**3 * 2**23] * 4
    maxnsupers = [8192, 131072] * 3 + [131072, 2097152] * 4
    COLLTSTEP = [1] * 6 + [0.1] * 4
    T_END = [3600] * 2 + [1800] * 4 + [3600] * 4

    config_filenames = []
    for r in range(nruns):
        cf = tmppath / f"config_{r}.yaml"
        shutil.copy(original_config, cf)
        config_filenames.append(cf)

        initsupers_filename = str(sharepath / f"dimlessSDsinit_{r}.dat")

        params = {
            "savefigpath": str(savefigpath),
            "sharepath": str(sharepath),
            "volexpr0": volexpr0[r],
            "numconc": numconc[r],
            "maxnsupers": maxnsupers[r],
            "COLLTSTEP": COLLTSTEP[r],
            "T_END": T_END[r],
            "constants_filename": str(constants_filename),
            "grid_filename": str(grid_filename),
            "initsupers_filename": initsupers_filename,
            "setup_filename": str(binpath / f"setup_{r}.txt"),
            "zarrbasedir": str(binpath / f"sol_{r}.zarr"),
        }
        editconfigfile.edit_config_params(cf, params)

    return config_filenames


def gridbox_boundaries(path2pySD, config_filename, isfigures=[False, False]):
    import sys
    import yaml
    from pathlib import Path

    sys.path.append(path2pySD)  # for imports from pySD package
    from pySD import geninitconds as gic

    config = yaml.safe_load(open(config_filename))
    pyconfig = config["python_initconds"]

    file2write = config["inputfiles"]["grid_filename"]
    if Path(file2write).is_file():
        msg = f"warning: skipping {file2write}, already exists"
        print(msg)
        return
    else:
        ### ----------------------- INPUT PARAMETERS ----------------------- ###
        ### --- essential paths and filenames --- ###
        constants_filename = config["inputfiles"]["constants_filename"]
        grid_filename = file2write
        savefigpath = Path(pyconfig["paths"]["savefigpath"])

        ### --- settings for 0-D Model gridbox boundaries --- ###
        zgrid = [0, 100, 100]
        xgrid = [0, 100, 100]
        ygrid = [0, 100, 100]
        ### ---------------------------------------------------------------- ###

        ### -------------------- INPUT FILES GENERATION -------------------- ###
        gic.generate_gridbox_boundaries(
            grid_filename,
            zgrid,
            xgrid,
            ygrid,
            constants_filename,
            isfigures=isfigures,
            savefigpath=savefigpath,
        )
        ### ---------------------------------------------------------------- ###


def initial_superdroplet_conditions(
    path2pySD, config_filename, isfigures=[False, False]
):
    import sys
    import yaml
    from pathlib import Path

    from .attrgens_shima2009 import SampleRadiiShima2009, SampleXiShima2009

    sys.path.append(path2pySD)  # for imports from pySD package
    from pySD.initsuperdropsbinary_src import (
        rgens,
        attrsgen,
    )
    from pySD import geninitconds as gic

    config = yaml.safe_load(open(config_filename))
    pyconfig = config["python_initconds"]

    file2write = config["initsupers"]["initsupers_filename"]
    if Path(file2write).is_file():
        msg = f"warning: skipping {file2write}, already exists"
        print(msg)
        return
    else:
        ### ----------------------- INPUT PARAMETERS ----------------------- ###
        ### --- essential paths and filenames --- ###
        initsupers_filename = file2write
        constants_filename = config["inputfiles"]["constants_filename"]
        grid_filename = config["inputfiles"]["grid_filename"]
        savefigpath = Path(pyconfig["paths"]["savefigpath"])
        savelabel = Path(initsupers_filename).stem

        ### --- number of gridboxes and uperdroplets per gridbox --- ###
        nsupers = int(config["domain"]["maxnsupers"])

        ### --- settings for initial superdroplets --- ###
        # settings for superdroplet attributes
        dryradius = pyconfig["supers"]["dryradius"]
        rspan = pyconfig["supers"]["rspan"]
        volexpr0 = pyconfig["supers"]["volexpr0"]
        numconc = pyconfig["supers"]["numconc"]

        # attribute generators
        radiigen = SampleRadiiShima2009(volexpr0, rspan)
        dryradiigen = rgens.MonoAttrGen(dryradius)
        xiprobdist = SampleXiShima2009()
        coord3gen = None
        coord1gen = None
        coord2gen = None
        initattrsgen = attrsgen.AttrsGenerator(
            radiigen, dryradiigen, xiprobdist, coord3gen, coord1gen, coord2gen
        )
        ### ---------------------------------------------------------------- ###

        ### -------------------- INPUT FILES GENERATION -------------------- ###
        gic.generate_initial_superdroplet_conditions(
            initattrsgen,
            initsupers_filename,
            config_filename,
            constants_filename,
            grid_filename,
            nsupers,
            numconc,
            isfigures=isfigures,
            savefigpath=savefigpath,
            gbxs2plt=0,
            savelabel=savelabel,
        )
        ### ---------------------------------------------------------------- ###
