#!/bin/bash

g++ -std=c++17 -Wall -Wextra -O2 ../monte-carlo/main_native.cpp ../monte-carlo/functions.cpp -o ../temp/native.exe || { echo "Compilation failed"; exit 1; }
