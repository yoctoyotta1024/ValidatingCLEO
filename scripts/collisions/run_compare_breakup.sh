#!/bin/bash
#SBATCH --job-name=compare_breakup
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=128
#SBATCH --mem=940M
#SBATCH --time=04:00:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0731
#SBATCH --output=./compare_breakup_out.%j.out
#SBATCH --error=./compare_breakup_err.%j.out

### ------------------ input parameters ---------------- ###
### ----- You need to edit these lines to specify ------ ###
### ----- your build configuration and executables ----- ###
### ---------------------------------------------------- ###
path2build=${1:-/work/mh0731/m300950/validating_cleo/build}     # should be absolute path
buildtype=${2:-openmp}                                          # "serial", "threads", "openmp" or "cuda"

SCRIPT_DIR=/home/m/m300950/validating_cleo/scripts
runscript=${SCRIPT_DIR}/run.sh

label="bucomp"
# label="bucomp_marshpam"  # only need runs 2,3,4 and 5 (straub efficiency)
### ---------------------------------------------------- ###

### ------------ run long executable ---------- ###
for run in 0; do
  runcmd="${runscript} ${path2build} ${buildtype} \
            /work/mh0731/m300950/validating_cleo/build/collisions/colls_long \
            /work/mh0731/m300950/validating_cleo/build/tmp/collisions/config_${label}_${run}.yaml"
  echo ${runcmd}
  eval ${runcmd}
done;
### -------------------------------------------------- ###

### ------------ run tesikstraub executable ---------- ###
for run in 1; do
  runcmd="${runscript} ${path2build} ${buildtype} \
            /work/mh0731/m300950/validating_cleo/build/collisions/colls_testikstraub \
            /work/mh0731/m300950/validating_cleo/build/tmp/collisions/config_${label}_${run}.yaml"
  echo ${runcmd}
  eval ${runcmd}
done;
### -------------------------------------------------- ###

### ------------ run straub_schlottke executable ---------- ###
for run in 2; do
  runcmd="${runscript} ${path2build} ${buildtype} \
            /work/mh0731/m300950/validating_cleo/build/collisions/colls_straub_schlottke \
            /work/mh0731/m300950/validating_cleo/build/tmp/collisions/config_${label}_${run}.yaml"
  echo ${runcmd}
  eval ${runcmd}
done;
### -------------------------------------------------- ###

### ------------ run straub_fixednfrags executable ---------- ###
for run in 3 4 5; do
  runcmd="${runscript} ${path2build} ${buildtype} \
            /work/mh0731/m300950/validating_cleo/build/collisions/colls_straub_fixednfrags \
            /work/mh0731/m300950/validating_cleo/build/tmp/collisions/config_${label}_${run}.yaml"
  echo ${runcmd}
  eval ${runcmd}
done;
### -------------------------------------------------- ###

### ------------ run constcoalbu_fixednfrags executable ---------- ###
for run in 6 7 8; do
  runcmd="${runscript} ${path2build} ${buildtype} \
            /work/mh0731/m300950/validating_cleo/build/collisions/colls_constcoalbu_fixednfrags \
            /work/mh0731/m300950/validating_cleo/build/tmp/collisions/config_${label}_${run}.yaml"
  echo ${runcmd}
  eval ${runcmd}
done;
### -------------------------------------------------- ###
