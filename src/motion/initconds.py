"""
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: initconds.py
Project: motion
Created Date: Thursday 17th April 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Thursday 24th April 2025
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Source files for script to generates input files for CLEO 2-D model of
divergence free flow similar to figure 1, Arabas et al. 2015
"""


def generate_configurations(path2pySD, path2build, original_config):
    import shutil
    import sys

    sys.path.append(str(path2pySD))  # for imports from pySD package
    from pySD import editconfigfile

    # parameters same for each run
    tmppath = path2build / "tmp" / "motion"
    sharepath = path2build / "share" / "motion"
    binpath = path2build / "bin" / "motion"
    savefigpath = binpath
    constants_filename = (
        path2build / "_deps" / "cleo-src" / "libs" / "cleoconstants.hpp"
    )

    # parameters specific for each run
    nruns = 3
    resolution = [100, 50, 25]
    MOTIONTSTEP = [1] * 3
    OBSTSTEP = [1] * 3
    ngbxs = [225, 900, 3600]
    nsupers_per_gbx = 128

    zgrid = [[0, 1500, r] for r in resolution]
    xgrid = [[0, 1500, r] for r in resolution]
    maxnsupers = [nsupers_per_gbx * n for n in ngbxs]

    config_filenames = []
    for r in range(nruns):
        cf = tmppath / f"config_{r}.yaml"
        shutil.copy(original_config, cf)
        config_filenames.append(cf)

        initsupers_filename = str(sharepath / f"dimlessSDsinit_{r}.dat")
        grid_filename = str(sharepath / f"dimlessGBxboundaries_{r}.dat")
        thermofiles = sharepath / f"dimlessthermo_{r}.dat"

        params = {
            "savefigpath": str(savefigpath),
            "sharepath": str(sharepath),
            "zgrid": zgrid[r],
            "xgrid": xgrid[r],
            "nsupers_per_gbx": nsupers_per_gbx,
            "thermofiles": str(thermofiles),
            "ngbxs": ngbxs[r],
            "maxnsupers": maxnsupers[r],
            "MOTIONTSTEP": MOTIONTSTEP[r],
            "OBSTSTEP": OBSTSTEP[r],
            "constants_filename": str(constants_filename),
            "grid_filename": str(grid_filename),
            "initsupers_filename": initsupers_filename,
            "setup_filename": str(binpath / f"setup_{r}.txt"),
            "zarrbasedir": str(binpath / f"sol_{r}.zarr"),
        }
        for var in ["press", "temp", "qvap", "qcond", "wvel", "uvel"]:
            var_filename = f"{thermofiles.stem}_{var}{thermofiles.suffix}"
            params[var] = str(thermofiles.parent / var_filename)

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

        ### --- number of gridboxes for label to save figure with --- ###
        ngbxs = config["domain"]["ngbxs"]
        savelabel = f"_{ngbxs}"

        ### --- settings for 0-D Model gridbox boundaries --- ###
        zgrid = pyconfig["grid"]["zgrid"]
        xgrid = pyconfig["grid"]["xgrid"]
        ygrid = pyconfig["grid"]["ygrid"]
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
            savelabel=savelabel,
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
        dryrgens,
        probdists,
        attrsgen,
        crdgens,
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

        ### --- settings for initial superdroplets --- ###
        # settings for superdroplet attributes
        nsupers = int(pyconfig["supers"]["nsupers_per_gbx"])
        mono_radius = float(pyconfig["supers"]["mono_radius"])
        numconc = pyconfig["supers"]["numconc"]

        # attribute generators
        radiigen = rgens.MonoAttrGen(mono_radius)
        dryradiigen = dryrgens.ScaledRadiiGen(1.0)
        xiprobdist = probdists.DiracDelta(mono_radius)
        coord3gen = crdgens.SampleCoordGen(True)
        coord1gen = crdgens.SampleCoordGen(True)
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


def thermodynamic_conditions(path2pySD, config_filename, isfigures=[False, False]):
    import sys
    import yaml
    from pathlib import Path

    sys.path.append(path2pySD)  # for imports from pySD package
    from pySD import geninitconds as gic
    from pySD.thermobinary_src import thermodyngen, thermogen

    config = yaml.safe_load(open(config_filename))
    pyconfig = config["python_initconds"]

    ### ----------------------- INPUT PARAMETERS ----------------------- ###
    ### --- essential paths and filenames --- ###
    thermofiles = Path(pyconfig["thermo"]["thermofiles"])
    constants_filename = config["inputfiles"]["constants_filename"]
    grid_filename = config["inputfiles"]["grid_filename"]
    savefigpath = Path(pyconfig["paths"]["savefigpath"])

    ### --- number of gridboxes for label to save figure with --- ###
    ngbxs = config["domain"]["ngbxs"]
    savelabel = f"_{ngbxs}"

    ### --- settings for thermodynamics and winds --- ###
    PRESS0 = pyconfig["thermo"]["PRESS0"]
    THETA = pyconfig["thermo"]["THETA"]
    Zbase = pyconfig["thermo"]["Zbase"]
    qvapmethod = pyconfig["thermo"]["qvapmethod"]
    qvaps = pyconfig["thermo"]["qvaps"]
    qcond_init = pyconfig["thermo"]["qcond_init"]
    moistlayer = False
    WMAX = pyconfig["thermo"]["WMAX"]
    Zlength = pyconfig["thermo"]["Zlength"]
    Xlength = pyconfig["thermo"]["Xlength"]
    VVEL = None

    # thermodynamics generator
    thermog = thermogen.DryHydrostaticAdiabatic2TierRelH(
        config_filename,
        constants_filename,
        PRESS0,
        THETA,
        qvapmethod,
        qvaps,
        Zbase,
        qcond_init,
        moistlayer,
    )
    windsg = thermog.create_default_windsgen(WMAX, Zlength, Xlength, VVEL)
    thermodyngen = thermodyngen.ThermodynamicsGenerator(thermog, windsg)
    ### ---------------------------------------------------------------- ###

    ### -------------------- INPUT FILES GENERATION -------------------- ###
    gic.generate_thermodynamics_conditions_fromfile(
        thermofiles,
        thermodyngen,
        config_filename,
        constants_filename,
        grid_filename,
        isfigures=isfigures,
        savefigpath=savefigpath,
        savelabel=savelabel,
    )
    ### ---------------------------------------------------------------- ###
