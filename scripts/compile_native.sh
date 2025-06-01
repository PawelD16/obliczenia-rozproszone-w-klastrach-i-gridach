#!/bin/bash

source .env

g++ -std=c++17 -Wall -Wextra -O3 -march=native  ../monte-carlo/main_native.cpp ../monte-carlo/functions.cpp -o $NATIVE_EXEC || { echo "Compilation failed"; exit 1; }
