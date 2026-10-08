#!/usr/bin/env python3
"""csv_converter.py — Convert a CSV file into JSON and Excel (.xlsx) formats.

Creates a sample products.csv, then writes products.json and products.xlsx
(using openpyxl). The Excel sheet keeps the header row bold.

Usage:
    python3 csv_converter.py
"""

import csv
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

BASE = Path(__file__).parent
INPUT_CSV = BASE / "products.csv"
OUTPUT_JSON = BASE / "products.json"
OUTPUT_XLSX = BASE / "products.xlsx"

SAMPLE_ROWS = [
    ["sku", "product", "price_pkr", "stock"],
    ["TX-001", "Toilet Tissue Roll", "85", "1200"],
    ["TX-002", "Paper Towel", "150", "800"],
    ["HW-001", "Hand Wash 1L", "350", "500"],
    ["SN-001", "Hand Sanitizer 500ml", "300", "650"],
    ["FL-001", "Floor Cleaner 1L", "280", "400"],
]


def create_sample() -> None:
    if not INPUT_CSV.exists():
        with open(INPUT_CSV, "w", newline="") as f:
            csv.writer(f).writerows(SAMPLE_ROWS)
        print(f"Sample file created: {INPUT_CSV}")


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def to_json(rows: list[dict], path: Path) -> None:
    with open(path, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"Wrote {path} ({len(rows)} records)")


def to_excel(rows: list[dict], path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Products"
    headers = list(rows[0].keys())
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for row in rows:
        ws.append([row[h] for h in headers])
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = 22
    wb.save(path)
    print(f"Wrote {path} ({len(rows)} rows)")


def main() -> None:
    create_sample()
    rows = read_csv(INPUT_CSV)
    print(f"Read {len(rows)} rows from {INPUT_CSV.name}")
    to_json(rows, OUTPUT_JSON)
    to_excel(rows, OUTPUT_XLSX)


if __name__ == "__main__":
    main()
