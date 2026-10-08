#!/usr/bin/env python3
"""csv_merger.py — Merge several CSV files into one, removing duplicate rows.

Creates 3 sample CSV files (customers_a.csv, customers_b.csv, customers_c.csv)
with overlapping rows, merges them into merged_customers.csv, and drops exact
duplicate rows (keeping the first occurrence).

Usage:
    python3 csv_merger.py
"""

import csv
from pathlib import Path

BASE = Path(__file__).parent
SAMPLES = BASE / "samples"
OUTPUT = BASE / "merged_customers.csv"

SAMPLE_DATA = {
    "customers_a.csv": [
        ["id", "name", "city"],
        ["1", "Ahmed Khan", "Lahore"],
        ["2", "Sara Malik", "Karachi"],
        ["3", "Usman Tariq", "Islamabad"],
    ],
    "customers_b.csv": [
        ["id", "name", "city"],
        ["3", "Usman Tariq", "Islamabad"],   # duplicate of a row in a
        ["4", "Ayesha Raza", "Lahore"],
        ["5", "Bilal Ahmed", "Faisalabad"],
    ],
    "customers_c.csv": [
        ["id", "name", "city"],
        ["5", "Bilal Ahmed", "Faisalabad"],  # duplicate of a row in b
        ["6", "Hina Shah", "Multan"],
        ["7", "Danish Ali", "Peshawar"],
    ],
}


def create_samples() -> list[Path]:
    SAMPLES.mkdir(exist_ok=True)
    paths = []
    for filename, rows in SAMPLE_DATA.items():
        path = SAMPLES / filename
        with open(path, "w", newline="") as f:
            csv.writer(f).writerows(rows)
        paths.append(path)
    return paths


def merge_csvs(paths: list[Path], output: Path) -> tuple[int, int]:
    """Merge CSVs, drop duplicate rows. Returns (rows_read, rows_written)."""
    seen: set[tuple] = set()
    header = None
    rows_read = 0
    unique_rows: list[list[str]] = []
    for path in paths:
        with open(path, newline="") as f:
            reader = csv.reader(f)
            file_header = next(reader)
            if header is None:
                header = file_header
            elif file_header != header:
                raise ValueError(f"Header mismatch in {path.name}")
            for row in reader:
                rows_read += 1
                key = tuple(row)
                if key not in seen:
                    seen.add(key)
                    unique_rows.append(row)
    with open(output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(unique_rows)
    return rows_read, len(unique_rows)


def main() -> None:
    paths = create_samples()
    print("Sample files created:")
    for p in paths:
        print(f"  - {p}")
    rows_read, rows_written = merge_csvs(paths, OUTPUT)
    print(f"\nRows read: {rows_read} | Unique rows written: {rows_written} "
          f"| Duplicates removed: {rows_read - rows_written}")
    print(f"Merged file: {OUTPUT}")


if __name__ == "__main__":
    main()
