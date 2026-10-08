#!/usr/bin/env python3
"""CSV Cleaner — clean up messy CSV files from the command line.

What it does:
  * Strips the UTF-8 BOM if present
  * Trims leading/trailing whitespace from every cell
  * Normalizes headers to lowercase_underscore style
    (e.g. "First Name" -> "first_name"; duplicates get _2, _3, ...)
  * Drops fully-empty rows
  * Drops duplicate rows (keeps the first occurrence)
  * Prints a stats report (rows in/out, rows dropped)

Usage:
    python csv_cleaner.py messy.csv
    python csv_cleaner.py messy.csv --output clean.csv
    python csv_cleaner.py messy.csv --dry-run

Only the Python standard library is used.
"""

import argparse
import csv
import os
import re
import sys


def normalize_header(name):
    """Turn a raw header into lowercase_underscore style."""
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)  # any non-alnum run -> _
    name = name.strip("_")
    return name or "column"


def clean_csv(path, output=None, dry_run=False):
    """Read, clean, report (and optionally write) the CSV. Returns exit code."""
    if not os.path.isfile(path):
        print(f"Error: input file not found: {path}", file=sys.stderr)
        return 1

    # utf-8-sig transparently strips a BOM if one exists
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))

    if not rows:
        print("Input file is empty.", file=sys.stderr)
        return 1

    raw_header, data_rows = rows[0], rows[1:]

    # Normalize headers, making duplicates unique (name, name_2, name_3, ...)
    headers = []
    seen_names = {}
    for raw in raw_header:
        norm = normalize_header(raw)
        if norm in seen_names:
            seen_names[norm] += 1
            norm = f"{norm}_{seen_names[norm]}"
        else:
            seen_names[norm] = 1
        headers.append(norm)
    n_cols = len(headers)

    # Trim cells, fix ragged rows, drop fully-empty rows
    trimmed = []
    empty_dropped = 0
    for row in data_rows:
        cells = [c.strip() if isinstance(c, str) else c for c in row]
        if len(cells) < n_cols:
            cells += [""] * (n_cols - len(cells))
        else:
            cells = cells[:n_cols]
        if all(c == "" for c in cells):
            empty_dropped += 1
            continue
        trimmed.append(cells)

    # Drop duplicate rows, keeping the first occurrence
    unique = []
    seen_rows = set()
    dup_dropped = 0
    for cells in trimmed:
        key = tuple(cells)
        if key in seen_rows:
            dup_dropped += 1
            continue
        seen_rows.add(key)
        unique.append(cells)

    rows_in = len(data_rows)
    rows_out = len(unique)

    print(f"Input:                 {path}")
    print(f"Headers normalized:    {', '.join(headers)}")
    print(f"Rows read:             {rows_in}")
    print(f"Empty rows dropped:    {empty_dropped}")
    print(f"Duplicate rows dropped:{dup_dropped:>4}")
    print(f"Rows written:          {rows_out}")

    if dry_run:
        print("(dry run - no file written)")
        return 0

    base, _ = os.path.splitext(path)
    out_path = output or f"{base}_cleaned.csv"
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(unique)
    print(f"Output:                {out_path}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Clean a CSV file: trim whitespace, normalize headers to "
                    "lowercase_underscore style, drop fully-empty rows and "
                    "duplicate rows, strip BOM, and print a stats report.",
        epilog="Example: python csv_cleaner.py messy.csv --output clean.csv",
    )
    parser.add_argument("input", help="Input CSV file to clean")
    parser.add_argument(
        "--output", "-o", default=None,
        help="Output CSV path (default: <input>_cleaned.csv)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the stats report without writing any file",
    )
    args = parser.parse_args()
    sys.exit(clean_csv(args.input, args.output, args.dry_run))


if __name__ == "__main__":
    main()
