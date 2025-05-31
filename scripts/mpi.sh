#!/bin/bash
#SBATCH --job-name=monte_carlo_mpi # set job name
#SBATCH --output=../output/mpi_%j.txt # set output file (%j is the job id)

# 1 node, 4 tasks (because 4 cores) not distributing betweend nodes
#SBATCH --ntasks=4
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1

source .env

mpirun $MPI_EXEC $A $TOTAL_SAMPLES

