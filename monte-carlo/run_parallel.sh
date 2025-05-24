#!/bin/bash
#SBATCH --job-name=monte_carlo_cpp # set job name
#SBATCH --output=monte_carlo_output_%j.txt # set output file (%j is the job id)

# 1 node, 4 tasks (because 4 cores) not distributing betweend nodes
#SBATCH --ntasks=4
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1

source .env

# compile code
g++ -std=c++17 -Wall -Wextra -O2 main.cpp functions.cpp -o monte_carlo.exe  || { echo "Compilation failed"; exit 1; }

# compute step size and sample size for subintervals
STEP=$(echo "($B - $A) / $SLURM_NTASKS" | bc -l)
SAMPLE_SIZE=$(echo "$TOTAL_SAMPLES / $SLURM_NTASKS" | bc -l)

# create a temporary directory for pipes
tmp_dir=$(mktemp -d)

declare -a pipes

for i in $(seq 0 $((SLURM_NTASKS - 1))); do
    A_i=$(echo "$A + $i * $STEP" | bc -l)
    B_i=$(echo "$A + ($i + 1) * $STEP" | bc -l)

    pipe="$tmp_dir/pipe_$i"
    mkfifo "$pipe"
    pipes[i]="$pipe"

    srun -n1 -c1 ./monte_carlo.exe "$A_i" "$B_i" "$SAMPLE_SIZE" > "$pipe" &
done

# read from pipes and sum results
total=0
for pipe in "${pipes[@]}"; do
    read val < "$pipe"
    total=$(echo "$total + $val" | bc -l)
    rm "$pipe"
done

rmdir "$tmp_dir"

echo "Final integral estimate: $total"
