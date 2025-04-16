'''
Copyright (c) 2025 MPI-M, Clara Bayley


----- ValidatingCLEO -----
File: initconds.py
Project: condevap
Created Date: Friday 11th April 2025
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
mono-size droplet distribution as in S. Arabas and S. Shima 2017.
'''

def generate_configurations(path2pySD, path2build, original_config):
    import shutil
    import sys
    import yaml

    sys.path.append(str(path2pySD))  # for imports from pySD package
    from pySD import editconfigfile

    # parameters same for each run
    tmppath = path2build / "tmp" / "condevap"
    sharepath = path2build / "share" / "condevap"
    binpath = path2build / "bin" / "condevap"
    savefigpath = binpath
    constants_filename = path2build / "_deps" / "cleo-src" / "libs" / "cleoconstants.hpp"
    grid_filename = sharepath / f"dimlessGBxboundaries.dat"

    # parameters specific for each run
    nruns = 9
    mono_radius = [1.0e-07] * 6 + [5.0e-08] * 3 
    numconc = [50.0e6] * 3 + [500.0e6] * 6
    CONDTSTEP = [1] * 9
    COUPLTSTEP = [1] * 9
    OBSTSTEP = [2] * 9
    T_END = [300, 600, 150000] * 3
    W_avg = [1, 0.5, 0.002] * 3
    TAU_half = [150, 300, 75000] * 3

    config_filenames = []
    for r in range(nruns):
        cf = tmppath / f"config_{r}.yaml"
        shutil.copy(original_config, cf)
        config_filenames.append(cf)
        
        initsupers_filename = str(sharepath / f"dimlessSDsinit_{r//3}.dat")

        params = {
            "savefigpath" : str(savefigpath),
            "sharepath" : str(sharepath),
            "mono_radius": mono_radius[r],
            "numconc" : numconc[r],
            "CONDTSTEP" : CONDTSTEP[r],
            "COUPLTSTEP" : COUPLTSTEP[r],
            "OBSTSTEP" : OBSTSTEP[r],
            "T_END" : T_END[r],
            "constants_filename" : str(constants_filename),
            "grid_filename" : str(grid_filename),
            "initsupers_filename" : initsupers_filename,
            "setup_filename" : str(binpath / f"setup_{r}.txt"),
            "zarrbasedir" : str(binpath / f"sol_{r}.zarr"),
            "W_avg" : W_avg[r],
            "TAU_half" : TAU_half[r],
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

        ### --- number of gridboxes and uperdroplets per gridbox --- ###
        nsupers = int(config["domain"]["maxnsupers"])

        ### --- settings for initial superdroplets --- ###
        # settings for superdroplet attributes
        mono_radius = float(pyconfig["supers"]["mono_radius"])
        numconc = pyconfig["supers"]["numconc"]

        # attribute generators
        radiigen = rgens.MonoAttrGen(mono_radius)
        dryradiigen = dryrgens.ScaledRadiiGen(1.0)
        xiprobdist = probdists.DiracDelta(mono_radius)
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
