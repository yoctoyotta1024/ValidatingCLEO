#!/bin/bash
#SBATCH --job-name=run
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=128
#SBATCH --mem=940M
#SBATCH --time=08:00:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./run_out.%j.out
#SBATCH --error=./run_err.%j.out

### same script as run_gpu.sh but with different SLURM settings

set -e
source /etc/profile
module purge
spack unload --all

### ------------------ input parameters ---------------- ###
### ----- You need to edit these lines to specify ------ ###
### ----- your build configuration and executables ----- ###
### ---------------------------------------------------- ###
path2build=${1:-/work/bm1183/m300950/validating_cleo/build}     # should be absolute path
buildtype=${2:-serial}                                          # "serial", "threads", "openmp" or "cuda"
executable2run=${3:-${path2build}/src/condevap/condevap}        # path to executable to run
configfile=${4:-${path2build}/tmp/condevap/config.yaml}         # configuration to run
enableyac=${5:-false}                                           # == "true" or otherwise false
stacksize_limit=${6:-204800}                                    # ulimit -s [stacksize_limit] (kB)

SCRIPT_DIR=/home/m/m300950/validating_cleo/scripts
bashsrc=${SCRIPT_DIR}/cleo/levante/bash/src
### ---------------------------------------------------- ###

### -------------------- check inputs ------------------ ###
if [[ "${path2build}" == "" || "${enableyac}" == "" || "${executable2run}" == "" ||
      "${configfile}" == "" || "${stacksize_limit}" == ""  ]]
then
  echo "Bad inputs, please check all the required inputs have been specified"
  exit 1
fi
### ---------------------------------------------------- ###

### ----------------- export inputs -------------------- ###
export CLEO_PATH2BUILD=${path2build}
export CLEO_BUILDTYPE=${buildtype}
export CLEO_ENABLEYAC=${enableyac}
### ---------------------------------------------------- ###

### -------------- print running inputs ---------------- ###
echo "### --------------- User Inputs -------------- ###"
echo "executable = ${executable2run}"
echo "config file for executable = ${configfile}"
echo "### ------------------------------------------- ###"
### ---------------------------------------------------- ###

### ------------------- run executable ----------------- ###
cd ${CLEO_PATH2BUILD} && pwd
runcmd="${SCRIPT_DIR}/cleo/levante/bash/run_cleo.sh ${executable2run} ${configfile} ${stacksize_limit}"
echo ${runcmd}
eval ${runcmd}
### -------------------------------------------------- ###
