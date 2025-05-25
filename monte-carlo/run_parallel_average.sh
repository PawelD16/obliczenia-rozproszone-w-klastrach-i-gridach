#!/bin/bash
#SBATCH --job-name=monte_carlo_cpp # set job name
#SBATCH --output=monte_carlo_output_%j.txt # set output file (%j is the job id)

# 1 node, 4 tasks (because 4 cores) not distributing betweend nodes
#SBATCH --ntasks=4
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1

source .env

# compile code
g++ -std=c++17 -Wall -Wextra -O2 main.cpp functions.cpp -o monte_carlo.exe || { echo "Compilation failed"; exit 1; }

# shared values
STEP=$(echo "($B - $A) / $SLURM_NTASKS" | bc -l)
SAMPLE_SIZE=$(echo "$TOTAL_SAMPLES / $SLURM_NTASKS" | bc -l)

# run each task with srun and collect results in parallel
# launch with srun and get result to pipe
srun --output=partial_output_%t.txt bash -c '
  ./monte_carlo.exe '"$A"' '"$B"' '"$SAMPLE_SIZE"'
'

# cleanup and aggregate
total=0
for f in partial_output_*.txt; do
  read val < "$f"
  total=$(echo "$total + $val" | bc -l)
  rm "$f"
done

result=$(echo "$total / $SLURM_NTASKS" | bc -l)

echo "Final integral estimate: $result"
