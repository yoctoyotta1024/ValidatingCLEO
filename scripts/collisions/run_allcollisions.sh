#!/bin/bash
#SBATCH --job-name=collisions
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=128
#SBATCH --mem=940M
#SBATCH --time=00:15:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./collisions_out.%j.out
#SBATCH --error=./collisions_err.%j.out

### ------------------ input parameters ---------------- ###
### ----- You need to edit these lines to specify ------ ###
### ----- your build configuration and executables ----- ###
### ---------------------------------------------------- ###
path2build=${1:-/work/bm1183/m300950/validating_cleo/build}     # should be absolute path
buildtype=${2:-openmp}                                          # "serial", "threads", "openmp" or "cuda"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
runscript=${SCRIPT_DIR}/../run.sh
### ---------------------------------------------------- ###

### -------------- run golovin executable -------------- ###
for run in 0 1; do
  runcmd="${runscript} ${path2build} ${buildtype} \
            /work/bm1183/m300950/validating_cleo/build/collisions/colls_golovin \
            /work/bm1183/m300950/validating_cleo/build/tmp/collisions/config_${run}.yaml"
  echo ${runcmd}
  eval ${runcmd}
done;
### -------------------------------------------------- ###

### --------------- run long executable --------------- ###
for run in 2 3 6 7; do
  runcmd="${runscript} ${path2build} ${buildtype} \
            /work/bm1183/m300950/validating_cleo/build/collisions/colls_long \
            /work/bm1183/m300950/validating_cleo/build/tmp/collisions/config_${run}.yaml"
  echo ${runcmd}
  eval ${runcmd}
done;
### -------------------------------------------------- ###

### ------------ run tesikstraub executable ---------- ###
for run in 4 5 8 9; do
  runcmd="${runscript} ${path2build} ${buildtype} \
            /work/bm1183/m300950/validating_cleo/build/collisions/colls_testikstraub \
            /work/bm1183/m300950/validating_cleo/build/tmp/collisions/config_${run}.yaml"
  echo ${runcmd}
  eval ${runcmd}
done;
### -------------------------------------------------- ###
