#!/bin/python3

import sys
import pandas as pd
from pathlib import Path


def analyze_csv(csv_path: str) -> None:
    """Analyze a CSV file containing Monte Carlo simulation results."""
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Calculate averages for each type
    for impl_type in df['type'].unique():
        type_data = df[df['type'] == impl_type]
        avg_runtime = type_data['runtime'].mean()
        avg_error = type_data['error'].mean()
        
        print(f"\n{impl_type.upper()} Implementation:")
        print(f"Average runtime: {avg_runtime:.3f} seconds")
        print(f"Average error: {avg_error:.6f}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python analyze_results.py <path_to_csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    if not Path(csv_path).exists():
        print(f"Error: File {csv_path} does not exist")
        sys.exit(1)

    print(f"\nAnalyzing {csv_path}")
    print("=" * 60)
    analyze_csv(csv_path)


if __name__ == "__main__":
    main()
