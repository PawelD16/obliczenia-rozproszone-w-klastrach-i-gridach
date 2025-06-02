#!/bin/python3

import subprocess
from typing import List

def run_experiment(n_points: int) -> None:
    print(f"\n{'='*60}")
    print(f"Running experiment with {n_points:,} points")
    print(f"{'='*60}\n")
    
    try:
        subprocess.run(["python3", "gather_results.py", "-n", str(n_points)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running experiment with {n_points} points: {e}")

def main() -> None:
    # Generate points from 1e8 to 1e9 with step 1e8
    points: List[int] = [int(i * 1e8) for i in range(1, 11)]
    
    for n_points in points:
        run_experiment(n_points)

if __name__ == "__main__":
    main() 