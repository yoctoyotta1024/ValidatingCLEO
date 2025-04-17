#!/bin/bash
#SBATCH --job-name=plotmotion
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./plot_motion.%j.out
#SBATCH --error=./plot_motion.%j.err

### ------------------ input parameters ---------------- ###
### ----- You need to edit these lines to specify ------ ###
### ----- your build configuration and executables ----- ###
### ---------------------------------------------------- ###
python=$1    # python to use (e.g. absolute path)
path2scripts=$2 # path to scripts dir or ValidateCLEO (should be absolute path)
path2CLEO=$3 # path to pySD dir of CLEO (should be absolute path)
path2bin=$4 # Absolute path to dataset and setup files
path4figs=$5 # Absolute path for directory to save plot(s) in"
### ---------------------------------------------------- ###

### ----------------- run python script ---------------- ###
${python} ${path2scripts}/scripts/motion/plot_results.py \
      ${path2CLEO} ${path2bin} ${path4figs}
### ---------------------------------------------------- ###
