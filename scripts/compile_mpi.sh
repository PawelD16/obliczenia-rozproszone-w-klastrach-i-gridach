#!/bin/bash

source .env

mpicxx -std=c++17 -Wall -Wextra -O3 -march=native -o $MPI_EXEC ../monte-carlo/main_mpi.cpp ../monte-carlo/functions.cpp || { echo "Compilation failed"; exit 1; }
