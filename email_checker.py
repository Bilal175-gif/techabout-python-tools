#!/usr/bin/env python3
"""email_checker.py — Find invalid email addresses in a CSV file.

Reads emails.csv (created as a sample on first run), validates each address
with a regex, and writes the invalid ones to invalid_emails.csv.

Usage:
    python3 email_checker.py
"""

import csv
import re
from pathlib import Path

BASE = Path(__file__).parent
INPUT_CSV = BASE / "emails.csv"
OUTPUT_CSV = BASE / "invalid_emails.csv"

EMAIL_RE = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

SAMPLE_ROWS = [
    ["name", "email"],
    ["Ahmed Khan", "ahmed.khan@example.com"],
    ["Sara Malik", "sara.malik@gmail.com"],
    ["Bad Entry 1", "not-an-email"],
    ["Usman Tariq", "usman.tariq@yahoo.com"],
    ["Bad Entry 2", "missing-at-sign.com"],
    ["Ayesha Raza", "ayesha.raza@company.pk"],
    ["Bad Entry 3", "user@.com"],
    ["Bilal Ahmed", "bilal.ahmed@outlook.com"],
    ["Bad Entry 4", "double@@at.com"],
    ["Hina Shah", "hina.shah@example.org"],
]


def is_valid(email: str) -> bool:
    return bool(EMAIL_RE.match(email.strip()))


def create_sample() -> None:
    if not INPUT_CSV.exists():
        with open(INPUT_CSV, "w", newline="") as f:
            csv.writer(f).writerows(SAMPLE_ROWS)
        print(f"Sample file created: {INPUT_CSV}")


def find_invalid(input_csv: Path, output_csv: Path) -> list[dict]:
    invalid: list[dict] = []
    with open(input_csv, newline="") as f:
        for row in csv.DictReader(f):
            email = row.get("email", "")
            if not is_valid(email):
                invalid.append(row)
                print(f"  INVALID: {email} ({row.get('name', '')})")
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email"])
        writer.writeheader()
        writer.writerows(invalid)
    return invalid


def main() -> None:
    create_sample()
    invalid = find_invalid(INPUT_CSV, OUTPUT_CSV)
    print(f"\nChecked emails.csv: {len(invalid)} invalid address(es) "
          f"written to {OUTPUT_CSV.name}")


if __name__ == "__main__":
    main()
