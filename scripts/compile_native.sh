#!/bin/bash

source vars.sh

g++ -std=c++17 -Wall -Wextra -O2 ../monte-carlo/main_native.cpp ../monte-carlo/functions.cpp -o $NATIVE_EXEC || { echo "Compilation failed"; exit 1; }
