#!/bin/bash

source prepare.sh
source compile_mpi.sh

echo $(sbatch mpi.sh)