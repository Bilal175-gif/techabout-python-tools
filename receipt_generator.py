#!/usr/bin/env python3
"""receipt_generator.py — Generate incremental receipt numbers like TAF-2026-0001.

The counter persists in receipt_counter.txt so numbers keep increasing across
runs. Format: TAF-<year>-<zero-padded 4-digit sequence>.

Usage:
    python3 receipt_generator.py          # prints the next receipt number
    python3 receipt_generator.py 2025      # use a custom year
"""

import sys
from pathlib import Path

COUNTER_FILE = Path(__file__).with_name("receipt_counter.txt")
PREFIX = "TAF"


def read_counter() -> int:
    if COUNTER_FILE.exists():
        try:
            return int(COUNTER_FILE.read_text().strip())
        except ValueError:
            return 0
    return 0


def write_counter(value: int) -> None:
    COUNTER_FILE.write_text(str(value))


def next_receipt(year: str = "2026") -> str:
    """Return the next receipt number and persist the incremented counter."""
    counter = read_counter() + 1
    write_counter(counter)
    return f"{PREFIX}-{year}-{counter:04d}"


def main() -> None:
    year = sys.argv[1] if len(sys.argv) > 1 else "2026"
    print(next_receipt(year))


if __name__ == "__main__":
    main()
