#!/bin/bash

source .env
source prepare.sh
source compile_native.sh

echo $(bash -c '
  '"$NATIVE_EXEC"' '"$A"' '"$SAMPLE_SIZE"'
')