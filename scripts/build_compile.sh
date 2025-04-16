#!/bin/bash
#SBATCH --job-name=buildcompile
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=128
#SBATCH --mem=940M
#SBATCH --time=00:05:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./buildcompile_out.%j.out
#SBATCH --error=./buildcompile_err.%j.out

### note: CLEO_PATH2CLEO here should be set as path to source directory, not CLEO libraries

set -e
source /etc/profile
module purge
spack unload --all

### ------------------ input parameters ---------------- ###
### ----- You need to edit these lines to specify ------ ###
### ----- your build configuration and executables ----- ###
### ---------------------------------------------------- ###
buildtype=${1:-serial}                         # "serial", "threads", "openmp" or "cuda"
compilername=${2:-intel}                       # "intel" or "gcc"
path2src=${3:-${HOME}/validating_cleo/src/}    # must be absolute path
path2build=${4:-/work/bm1183/m300950/validating_cleo/build}  # should be absolute path
build_flags=${5:-"-DCLEO_COUPLED_DYNAMICS="""} # CLEO_BUILD_FLAGS
executables=${6:-"NONE"}                       # list of executables to compile or "NONE"
enabledebug=${7:-false}                        # == "true" or otherwise false
enableyac=${8:-false}                          # == "true" or otherwise false
yacyaxtroot=${9:-/work/bm1183/m300950/yacyaxt} # yac and yaxt in yacyaxtroot/yac and yacyaxtroot/yaxt
make_clean=${10:-true}                         # == "true" or otherwise false

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
bashsrc=${SCRIPT_DIR}/cleo/levante/bash/src
### ---------------------------------------------------- ###

### ------------------ check arguments ----------------- ###
if [ "${path2src}" == "" ]
then
  echo "Please provide path to source directory"
  exit 1
fi
source ${bashsrc}/check_inputs.sh
check_args_not_empty "${buildtype}" "${compilername}" "${enabledebug}" "${path2src}" "${path2build}" "${enableyac}"
### ---------------------------------------------------- ###

### ----------------- export inputs -------------------- ###
export CLEO_BUILDTYPE=${buildtype}
export CLEO_COMPILERNAME=${compilername}
export CLEO_PATH2CLEO=${path2src}
export CLEO_PATH2BUILD=${path2build}
export CLEO_BUILD_FLAGS=${build_flags}
export CLEO_ENABLEDEBUG=${enabledebug}
export CLEO_ENABLEYAC=${enableyac}

if [ ${CLEO_ENABLEYAC} == "true" ]
then
  export CLEO_YACYAXTROOT=${yacyaxtroot}
fi
### ---------------------------------------------------- ###

### -------------------- check inputs ------------------ ###
check_source_and_build_paths
check_buildtype
check_compilername
check_yac
### ---------------------------------------------------- ###

### -------------------- print inputs ------------------- ###
echo "### --------------- User Inputs -------------- ###"
echo "CLEO_BUILDTYPE = ${CLEO_BUILDTYPE}"
echo "CLEO_COMPILERNAME = ${CLEO_COMPILERNAME}"
echo "CLEO_PATH2CLEO = ${CLEO_PATH2CLEO}"
echo "CLEO_PATH2BUILD = ${CLEO_PATH2BUILD}"
echo "CLEO_BUILD_FLAGS = ${CLEO_BUILD_FLAGS}"
echo "CLEO_ENABLEDEBUG = ${CLEO_ENABLEDEBUG}"
echo "CLEO_ENABLEYAC = ${CLEO_ENABLEYAC}"
echo "CLEO_YACYAXTROOT = ${CLEO_YACYAXTROOT}"
echo "executables = ${executables}"
echo "### ------------------------------------------- ###"
### ---------------------------------------------------- ###

### --------------------- build CLEO ------------------- ###
buildcmd="${SCRIPT_DIR}/cleo/levante/bash/build_cleo.sh"
echo ${buildcmd}
eval ${buildcmd}
### ---------------------------------------------------- ###

### ---------------- compile executables --------------- ###
compilecmd="${SCRIPT_DIR}/cleo/levante/bash/compile_cleo.sh \"${executables}\" ${make_clean}"
echo ${compilecmd}
eval ${compilecmd}
### ---------------------------------------------------- ###
