#!/bin/bash

mpicxx -o ../temp/mpi.exe ../monte-carlo/main_mpi.cpp ../monte-carlo/functions.cpp || { echo "Compilation failed"; exit 1; }
