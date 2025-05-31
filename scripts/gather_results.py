#!/bin/python3

import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv

from Result import Result

load_dotenv()

LOG_FILE = os.getenv("LOG_FILE")
CSV_FILENAME = os.getenv("CSV_FILENAME")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
ENV_RUN_REPETITIONS = os.getenv("RUN_REPETITIONS")
RUN_REPETITIONS = int(ENV_RUN_REPETITIONS) if ENV_RUN_REPETITIONS else 10

NATIVE_SCRIPT_PATH = "run_native_simple.sh"
MPI_SCRIPT_PATH = "run_mpi_simple.sh"
NO_PARALLELZATION_SCRIPT_PATH = "run_no_parallelization.sh"


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


def read_log_file_runtimes(pathname: str | None) -> Dict[str, float]:
    runtimes: Dict[str, float] = {}

    if not pathname:
        return runtimes

    with open(pathname, "r") as f:
        for line in f:
            fields = dict(entry.split("=") for entry in line.strip().split() if "=" in entry)
            job_id = fields.get("JobId")
            start = fields.get("StartTime")
            end = fields.get("EndTime")

            if job_id and start and end:
                try:
                    start_time = datetime.fromisoformat(start)
                    end_time = datetime.fromisoformat(end)
                    runtime_seconds = (end_time - start_time).total_seconds()
                    runtimes[job_id] = runtime_seconds
                except ValueError:
                    print(f"Invalid timestamp for job {job_id}")

    return runtimes


def write_runtimes_to_csv(results: List[Result], output_csv: str) -> None:
    with open(output_csv, 'w', newline='') as csvfile:
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


def run_job(pathname: str) -> str:
    result: subprocess.CompletedProcess[str] = subprocess.run(["bash", pathname], capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Failed to submit job: {result.stderr}")

    match = re.search(r"Submitted batch job (\d+)", result.stdout)

    if not match:
        raise RuntimeError("Could not parse job ID from sbatch output")

    return match.group(1)


def process_job(pathname: str) -> Result:
    job_id = run_job(pathname)
    wait_for_job_completion(job_id)

    res_object = Result(job_id)
    res_object.result = float(get_job_output(job_id, OUTPUT_DIR).strip())

    return res_object


def main() -> None:
    clear_log_file(LOG_FILE)

    results: List[Result] = []

    for idx in range(0, RUN_REPETITIONS):
        res = process_job(NATIVE_SCRIPT_PATH)
        res.type = "native"
        results.append(res)

        res = process_job(MPI_SCRIPT_PATH)
        res.type = "mpi"
        results.append(res)

    runtimes = read_log_file_runtimes(LOG_FILE)

    for result in results:
        if result.job_id not in runtimes:
            raise RuntimeError(f"Could find runtime for {result.job_id}")

        result.runtime = runtimes[result.job_id]


if __name__ == "__main__":
    main()
