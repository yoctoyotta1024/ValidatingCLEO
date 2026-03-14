"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: initconds_compare_breakup.py
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
Script generates input files for CLEO 0-D box model with
droplet distribution as in Shima et al. 2009 for
comparison study with de Jong et al. 2023.
"""


def generate_configurations(
    path2pySD, path2build, original_config, use_marshall_parmer
):
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

    if use_marshall_parmer:
        grid_filename = sharepath / "dimlessGBxboundaries_bucomp_marshpam.dat"
    else:
        grid_filename = sharepath / "dimlessGBxboundaries_bucomp.dat"

    # parameters specific for each run
    nruns = (
        9  # [long, testikstraub+schlottke, straub+schlottke, 3x straub, 3x constcoalbu]
    )
    if use_marshall_parmer:
        volexpr0 = ["n/a"] * nruns
        numconc = ["XXX"] * nruns
    if not use_marshall_parmer:
        volexpr0 = [30.531e-06] * nruns
        numconc = [100e6] * nruns
    maxnsupers = [8192] * nruns
    COLLTSTEP = [1] * nruns
    OBSTSTEP = [10] + [60] * 5 + [10] * 3
    T_END = [240] + [7200] * 5 + [240] * 3
    nfrags = [0, 0, 0] + [2.51, 4, 8, 4, 16, 64]
    coaleff = [1.0] * 6 + [0.95] * 3

    config_filenames = []
    for r in range(nruns):
        label = "bucomp"
        if use_marshall_parmer:
            label += "_marshpam"
        cf = tmppath / f"config_{label}_{r}.yaml"
        shutil.copy(original_config, cf)
        config_filenames.append(cf)

        initsupers_filename = str(sharepath / f"dimlessSDsinit_{label}_{r}.dat")

        params = {
            "savefigpath": str(savefigpath),
            "sharepath": str(sharepath),
            "volexpr0": volexpr0[r],
            "numconc": numconc[r],
            "maxnsupers": maxnsupers[r],
            "COLLTSTEP": COLLTSTEP[r],
            "OBSTSTEP": OBSTSTEP[r],
            "T_END": T_END[r],
            "constants_filename": str(constants_filename),
            "grid_filename": str(grid_filename),
            "initsupers_filename": initsupers_filename,
            "setup_filename": str(binpath / f"setup_{label}_{r}.txt"),
            "zarrbasedir": str(binpath / f"sol_{label}_{r}.zarr"),
            "coaleff": coaleff[r],
            "nfrags": nfrags[r],
            "use_marshall_parmer": use_marshall_parmer,
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
        if pyconfig["supers"]["use_marshall_parmer"]:
            grid_spacing = [0, 100, 100]  # (!) must be consistent with ``volume'' below
        else:
            grid_spacing = [0, 10, 10]
        zgrid = xgrid = ygrid = grid_spacing
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

    sys.path.append(path2pySD)  # for imports from pySD package
    from pySD.initsuperdropsbinary_src import (
        rgens,
        probdists,
        attrsgen,
    )
    from pySD import geninitconds as gic

    from .probdists_marshallpalmer import get_marshall_palmer_generators

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
        if pyconfig["supers"]["use_marshall_parmer"]:
            volume = 100**3  # (!) must be consistent with grid above [m^3]
            rspan = [5e-7, 4e-3]  # [m]
            radiigen, xiprobdist = get_marshall_palmer_generators(rspan, volume)
            numconc = xiprobdist.calc_numconc()
        else:
            rspan = [5e-6, 7e-5]
            volexpr0 = pyconfig["supers"]["volexpr0"]
            numconc = pyconfig["supers"]["numconc"]
            xiprobdist = probdists.VolExponential(volexpr0, rspan)
            radiigen = rgens.SampleLog10RadiiGen(rspan)

        # attribute generators
        dryradiigen = rgens.MonoAttrGen(dryradius)
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
