#!/bin/bash

source prepare.sh
source compile_native.sh

echo $(sbatch native.sh)