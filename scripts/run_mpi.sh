#!/bin/bash

source prepare.sh

source compile_mpi.sh

echo "Current time: $(date)"

sbatch mpi.sh
