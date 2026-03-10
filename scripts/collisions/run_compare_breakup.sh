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
### ---------------------------------------------------- ###

### ------------ run tesikstraub executable ---------- ###
for run in 0; do
  runcmd="${runscript} ${path2build} ${buildtype} \
            /work/mh0731/m300950/validating_cleo/build/collisions/colls_testikstraub \
            /work/mh0731/m300950/validating_cleo/build/tmp/collisions/config_bucomp_${run}.yaml"
  echo ${runcmd}
  eval ${runcmd}
done;
### -------------------------------------------------- ###

### ------------ run tesikstraub_fixednfrags executable ---------- ###
for run in 1 2 3; do
  runcmd="${runscript} ${path2build} ${buildtype} \
            /work/mh0731/m300950/validating_cleo/build/collisions/colls_straub_fixednfrags \
            /work/mh0731/m300950/validating_cleo/build/tmp/collisions/config_bucomp_${run}.yaml"
  echo ${runcmd}
  eval ${runcmd}
done;
### -------------------------------------------------- ###
