#!/usr/bin/env python3
"""donation_totals.py — Read a mock donations CSV and print summary statistics.

Creates a sample donations.csv (donor, amount_pkr, date), then prints:
total donated, average donation, and the largest single donation.

Usage:
    python3 donation_totals.py
"""

import csv
from pathlib import Path

BASE = Path(__file__).parent
INPUT_CSV = BASE / "donations.csv"

SAMPLE_ROWS = [
    ["donor", "amount_pkr", "date"],
    ["Ahmed Khan", "5000", "2026-09-01"],
    ["Sara Malik", "12000", "2026-09-03"],
    ["Usman Tariq", "7500", "2026-09-05"],
    ["Ayesha Raza", "25000", "2026-09-10"],
    ["Bilal Ahmed", "3000", "2026-09-12"],
    ["Hina Shah", "15000", "2026-09-15"],
    ["Danish Ali", "8000", "2026-09-18"],
    ["Fatima Noor", "20000", "2026-09-20"],
]


def create_sample() -> None:
    if not INPUT_CSV.exists():
        with open(INPUT_CSV, "w", newline="") as f:
            csv.writer(f).writerows(SAMPLE_ROWS)
        print(f"Sample file created: {INPUT_CSV}")


def summarize(path: Path) -> dict:
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    amounts = [float(r["amount_pkr"]) for r in rows]
    return {
        "count": len(amounts),
        "total": sum(amounts),
        "average": sum(amounts) / len(amounts) if amounts else 0,
        "largest": max(amounts) if amounts else 0,
    }


def main() -> None:
    create_sample()
    stats = summarize(INPUT_CSV)
    print(f"Donations file : {INPUT_CSV.name}")
    print(f"Donations count: {stats['count']}")
    print(f"Total donated  : PKR {stats['total']:,.0f}")
    print(f"Average gift   : PKR {stats['average']:,.0f}")
    print(f"Largest gift   : PKR {stats['largest']:,.0f}")


if __name__ == "__main__":
    main()
