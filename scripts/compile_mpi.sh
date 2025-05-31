#!/bin/bash

source .env

mpicxx -o $MPI_EXEC ../monte-carlo/main_mpi.cpp ../monte-carlo/functions.cpp || { echo "Compilation failed"; exit 1; }
