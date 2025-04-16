#!/bin/bash
#SBATCH --job-name=compileonly
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=128
#SBATCH --mem=940M
#SBATCH --time=00:05:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./compileonly_out.%j.out
#SBATCH --error=./compileonly_err.%j.out

### note: CLEO_PATH2CLEO here should be set as path to source directory, not CLEO libraries

set -e
source /etc/profile
module purge
spack unload --all

### ------------------ input parameters ---------------- ###
### ----- You need to edit these lines to specify ------ ###
### ----- your build configuration and executables ----- ###
### ---------------------------------------------------- ###
executables=${1:-"NONE"}                                        # executable(s) to compile
buildtype=${2:-serial}                                          # "serial", "threads", "openmp" or "cuda"
compilername=${3:-intel}                                        # "intel" or "gcc"
path2src=${4:-${HOME}/validating_cleo/src/}                     # must be absolute path
path2build=${5:-/work/bm1183/m300950/validating_cleo/build}     # should be absolute path
enableyac=${6:-false}                                           # == "true" or otherwise false
make_clean=${7:-false}                                          # == "true" or otherwise false

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
### ---------------------------------------------------- ###

### -------------------- check inputs ------------------ ###
if [[ "${buildtype}" == "" || "${compilername}" == "" || "${enableyac}" == "" ||
      "${path2src}" == "" || "${path2build}" == ""  ]]
then
  echo "Bad inputs, please check all the required inputs have been specified"
  exit 1
fi

if [[ "${path2src}" == "${path2build}" ]]
then
  echo "Bad inputs, build directory cannot match the path to CLEO source"
  exit 1
fi

if [ "${buildtype}" != "serial" ] &&
   [ "${buildtype}" != "openmp" ] &&
   [ "${buildtype}" != "threads" ] &&
   [ "${buildtype}" != "cuda" ];
then
  echo "Bad inputs, build type must be 'serial', 'openmp', 'threads' or 'cuda'"
  exit 1
fi
### ---------------------------------------------------- ###

### ----------------- export inputs -------------------- ###
export CLEO_BUILDTYPE=${buildtype}
export CLEO_COMPILERNAME=${compilername}
export CLEO_PATH2CLEO=${path2src}
export CLEO_PATH2BUILD=${path2build}
export CLEO_ENABLEYAC=${enableyac}
### ---------------------------------------------------- ###

### --------------- print compiling inputs ------------- ###
echo "### --------------- User Inputs -------------- ###"
echo "CLEO_BUILDTYPE = ${CLEO_BUILDTYPE}"
echo "CLEO_COMPILERNAME = ${CLEO_COMPILERNAME}"
echo "CLEO_PATH2BUILD = ${CLEO_PATH2BUILD}"
echo "CLEO_ENABLEYAC = ${CLEO_ENABLEYAC}"
echo "### ------------------------------------------- ###"
### ---------------------------------------------------- ###

### ---------------- compile executables --------------- ###
compilecmd="${SCRIPT_DIR}/cleo/levante/bash/compile_cleo.sh \"${executables}\" ${make_clean}"
echo ${compilecmd}
eval ${compilecmd}
### ---------------------------------------------------- ###
