#!/bin/bash 
###############################################################################
#SBATCH -N 5
#SBATCH --ntasks-per-node=64
#SBATCH --ntasks=320
#SBATCH -t 1-00:00:00
#SBATCH -o mfc_test_%A.out
#SBATCH -J mfc_test
#SBATCH --exclusive

###############################################################################
## Modules
module swap gnu9/9.4.0 gcc
module load python fftw cmake
module load openmpi/4.1.5
module load anaconda/3.0
conda activate MFC_env


## Running MFC
cd /home/gamertjb/MFC_three_fluid_surface_tension/
./mfc.sh run --debug /home/gamertjb/MFC_three_fluid_surface_tension/examples/2D_jet_SK/case.py -b mpirun -n 320
