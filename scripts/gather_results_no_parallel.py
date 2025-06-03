#!/bin/python3

import os
import subprocess
import time
import argparse
from typing import List
import math

from dotenv import load_dotenv
from Result import Result

load_dotenv()

CSV_FILENAME = os.getenv("CSV_FILENAME", "results_no_parallel.csv")
ENV_RUN_REPETITIONS = os.getenv("RUN_REPETITIONS")
RUN_REPETITIONS = int(ENV_RUN_REPETITIONS) if ENV_RUN_REPETITIONS else 10
A = float(os.getenv("A", "1.0"))  # radius from environment


def parse_args():
    parser = argparse.ArgumentParser(description='Run Monte Carlo simulations with no parallelization')
    parser.add_argument('-n', '--num-points', type=int,
                       default=int(os.getenv("TOTAL_SAMPLES", "1000000")),
                       help='Number of points to use in simulation (default: from TOTAL_SAMPLES env or 1000000)')
    return parser.parse_args()


def get_theoretical_area(radius: float) -> float:
    """Calculate the theoretical area that matches the C++ implementation.
    The C++ code returns (points_in_square_and_circle / total_points) * πr²
    = (1/2) * πr² = (π/2)r²"""
    return (math.pi / 2.0) * (radius ** 2)


def get_power_of_ten(n: int) -> int:
    """Get the power of 10 for a number (e.g., 100000000 -> 8 because 10^8)."""
    return len(str(n)) - 1


def run_single_experiment(total_samples: int) -> Result:
    """Run a single experiment and measure its execution time."""
    start_time = time.time()
    
    # Run the experiment and capture its output
    result = subprocess.run(
        ["bash", "run_no_parralellization.sh"],
        capture_output=True,
        text=True,
        env={**os.environ, "TOTAL_SAMPLES": str(total_samples)}
    )
    
    end_time = time.time()
    
    if result.returncode != 0:
        raise RuntimeError(f"Experiment failed: {result.stderr}")
    
    # Create a Result object with a dummy job ID (since we're not using SLURM)
    res = Result(f"no_parallel_{int(start_time)}", float(result.stdout.strip()))
    res.runtime = end_time - start_time
    
    return res


def write_runtimes_to_csv(results: List[Result], output_csv: str) -> None:
    with open(output_csv, "w", newline="") as csvfile:
        csvfile.write("\n".join(Result.to_csv_list(results)))


def main() -> None:
    args = parse_args()
    total_samples = args.num_points
    print(f"Running with {total_samples:,} points")

    # Modify CSV filename to include the power of 10
    power = get_power_of_ten(total_samples)
    csv_path = CSV_FILENAME.replace('.csv', f'_{power}.csv')

    results: List[Result] = []
    theoretical = get_theoretical_area(A)

    for i in range(RUN_REPETITIONS):
        print(f"\nRunning experiment {i+1}/{RUN_REPETITIONS}")
        res = run_single_experiment(total_samples)
        res.type = "no_parallel"
        res.calculate_error(theoretical)
        results.append(res)
        print(f"Runtime: {res.runtime:.2f}s")

    write_runtimes_to_csv(results, csv_path)
    print(f"\nResults saved to {csv_path}")


if __name__ == "__main__":
    main() 