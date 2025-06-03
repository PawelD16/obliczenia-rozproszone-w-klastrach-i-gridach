#!/bin/python3

import os
import re
import subprocess
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from statistics import mean
import math

from dotenv import load_dotenv

from Result import Result

load_dotenv()

LOG_FILE = os.getenv("LOG_FILE")
CSV_FILENAME = os.getenv("CSV_FILENAME")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
ENV_RUN_REPETITIONS = os.getenv("RUN_REPETITIONS")
RUN_REPETITIONS = int(ENV_RUN_REPETITIONS) if ENV_RUN_REPETITIONS else 10
A = float(os.getenv("A", "1.0"))  # radius from environment


def parse_args():
    parser = argparse.ArgumentParser(description='Run Monte Carlo simulations with native and MPI implementations')
    parser.add_argument('-n', '--num-points', type=int,
                       default=int(os.getenv("TOTAL_SAMPLES", "1000000")),
                       help='Number of points to use in simulation (default: from TOTAL_SAMPLES env or 1000000)')
    return parser.parse_args()


NATIVE_SCRIPT_PATH = "run_native_simple.sh"
MPI_SCRIPT_PATH = "run_mpi_simple.sh"
NO_PARALLELZATION_SCRIPT_PATH = "run_no_parallelization.sh"


def get_theoretical_area(radius: float) -> float:
    """Calculate the theoretical area that matches the C++ implementation.
    The C++ code returns (points_in_square_and_circle / total_points) * πr²
    = (1/2) * πr² = (π/2)r²"""
    return (math.pi / 2.0) * (radius ** 2)


def calculate_average_error(results: List[Result], result_type: str) -> float:
    """Calculate average absolute error for given type of results."""
    theoretical = get_theoretical_area(A)
    errors = [abs(r.result - theoretical) for r in results if r.type == result_type]
    return mean(errors) if errors else 0.0


def clear_log_file(pathname: str | None) -> None:
    if not pathname:
        return

    jobcomp_file = Path(pathname)

    try:
        jobcomp_file.write_text("")
        print(f"Cleared job comp file: {jobcomp_file}")
    except PermissionError:
        print("Permission denied. Try running with sudo or check file ownership.")
    except Exception as e:
        print(f"Error: {e}")


def read_log_file_runtimes(file_path: str | None) -> Dict[str, float]:
    if not file_path:
        raise FileNotFoundError(f"Couldn't find {file_path} log file")

    results: Dict[str, float] = {}

    with open(file_path, "r") as f:
        for line in f:
            fields = {}
            for entry in line.strip().split():
                if "=" in entry:
                    key, value = entry.split("=", 1)
                    fields[key] = value

            job_id = fields.get("JobId")
            state: str = fields.get("JobState", "")
            start = fields.get("StartTime")
            end = fields.get("EndTime")

            if job_id and start and end and state.upper() == "COMPLETED":
                try:
                    start_time = datetime.fromisoformat(start)
                    end_time = datetime.fromisoformat(end)
                    runtime = (end_time - start_time).total_seconds()
                    results[job_id] = runtime
                except ValueError:
                    print(f"Invalid date format for job {job_id}")
    return results


def write_runtimes_to_csv(results: List[Result], output_csv: str) -> None:
    # Ensure the results directory exists
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", newline="") as csvfile:
        csvfile.write("\n".join(Result.to_csv_list(results)))


def wait_for_job_completion(job_id: str, poll_interval=2) -> None:
    print(f"Waiting for finish of {job_id}")

    while True:
        result = subprocess.run(["squeue", "-j", job_id], capture_output=True, text=True)
        if job_id not in result.stdout:
            return
        time.sleep(poll_interval)


def get_job_output(job_id: str, output_dir: str | None = ".") -> str:
    actual_output_dir = output_dir or "."
    matches = list(Path(actual_output_dir).glob(f"*{job_id}*"))

    if not matches:
        raise FileNotFoundError(f"No file found matching pattern '*{job_id}*' in {actual_output_dir}")
    if len(matches) > 1:
        print(f"Warning: multiple matches found. Using first: {matches[0].name}")

    return matches[0].read_text()


def run_job(pathname: str, total_samples: int) -> str:
    # Set environment variables for this run
    env = os.environ.copy()
    env["TOTAL_SAMPLES"] = str(total_samples)
    
    result = subprocess.run(["bash", pathname], capture_output=True, text=True, env=env)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to submit job: {result.stderr}")

    match = re.search(r"Submitted batch job (\d+)", result.stdout)

    if not match:
        raise RuntimeError("Could not parse job ID from sbatch output")

    return match.group(1)


def process_job(pathname: str, total_samples: int) -> Result:
    if pathname == NO_PARALLELZATION_SCRIPT_PATH:
        # For no parallelization, measure time directly
        start_time = time.time()
        result = subprocess.run(
            ["bash", pathname],
            capture_output=True,
            text=True,
            env={**os.environ, "TOTAL_SAMPLES": str(total_samples)}
        )
        end_time = time.time()
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to run no-parallel job: {result.stderr}")
            
        res_object = Result(f"no_parallel_{int(start_time)}", float(result.stdout.strip()))
        res_object.runtime = end_time - start_time
        return res_object
    else:
        # For MPI and native versions, use SLURM
        job_id = run_job(pathname, total_samples)
        wait_for_job_completion(job_id)
        res_object = Result(job_id, float(get_job_output(job_id, OUTPUT_DIR).strip()))
        return res_object


def main() -> None:
    args = parse_args()
    total_samples = args.num_points
    print(f"Running with {total_samples:,} points")

    # Modify CSV filename to include the number
    num = total_samples / 1e8
    csv_path = str(CSV_FILENAME).replace('.csv', f'_{num}.csv')

    clear_log_file(LOG_FILE)
    results: List[Result] = []
    theoretical = get_theoretical_area(A)

    for _ in range(0, RUN_REPETITIONS):
        # Run native version
        res = process_job(NATIVE_SCRIPT_PATH, total_samples)
        res.type = "native"
        res.calculate_error(theoretical)
        results.append(res)

        # Run MPI version
        res = process_job(MPI_SCRIPT_PATH, total_samples)
        res.type = "mpi"
        res.calculate_error(theoretical)
        results.append(res)

        # Run no parallelization version
        res = process_job(NO_PARALLELZATION_SCRIPT_PATH, total_samples)
        res.type = "no_parallel"
        res.calculate_error(theoretical)
        results.append(res)

    runtimes = read_log_file_runtimes(LOG_FILE)

    # Update runtimes for SLURM jobs (native and mpi)
    for result in results:
        if result.type != "no_parallel":  # Skip no_parallel as it already has runtime
            if result.job_id not in runtimes:
                raise RuntimeError(f"Could find runtime for {result.job_id}")
            result.runtime = runtimes[result.job_id]

    write_runtimes_to_csv(results, csv_path)


if __name__ == "__main__":
    main()
