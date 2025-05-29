#!/bin/bash

source prepare.sh

source compile_native.sh

echo "Current time: $(date)"

sbatch native.sh