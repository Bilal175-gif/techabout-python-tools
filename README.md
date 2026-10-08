# Python Tools — TechAbout

A collection of small, practical Python utilities built for everyday office
and data tasks. Every script is self-contained and creates its own sample
data so you can run it immediately.

Built for [BlogReach.com](https://blogreach.com) — guest-posting marketplace.

## Requirements

- Python 3.8+ (tested with Python 3.12)
- `openpyxl` — only for `csv_converter.py`: `pip install openpyxl`
- `pytest` — only to run the tests: `pip install pytest`
- Everything else uses the standard library.

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for virtual-environment setup.

---

## 1. CSV Cleaner (`csv_cleaner.py`)

Cleans a messy CSV file:

- Strips the UTF-8 BOM if present
- Trims leading/trailing whitespace from every cell
- Normalizes headers to `lowercase_underscore` style
  (`"First Name"` → `first_name`; clashing names become `name_2`, `name_3`, …)
- Drops fully-empty rows
- Drops duplicate rows (keeps the first occurrence)
- Prints a stats report: rows read, empty rows dropped, duplicates dropped, rows written

### Usage

```bash
# Show the stats report without writing anything
python csv_cleaner.py sample.csv --dry-run

# Clean and write to <input>_cleaned.csv
python csv_cleaner.py sample.csv

# Clean and write to a chosen file
python csv_cleaner.py sample.csv --output clean.csv

# Full help
python csv_cleaner.py --help
```

### Example

`python csv_cleaner.py sample.csv --output cleaned_sample.csv` produces:

```
first_name,last_name,email,age,city
Ahmed,Khan,ahmed@example.com,30,Lahore
Sara,Malik,sara@example.com,25,Karachi
Bilal,Shah,bilal@example.com,28,Lahore
Ali,Raza,ali@example.com,35,Islamabad
```

with the report: 8 rows read → 2 empty dropped → 2 duplicates dropped → 4 rows written.

---

## 2. URL Status Checker (`url_status_checker.py`)

Checks HTTP status of many URLs concurrently and reports, per URL:

- HTTP status code (`200`, `404`, … or `ERROR` if unreachable)
- Final URL after following redirects
- Response time in seconds

URLs can come from command-line arguments, a text file (`--file`, one URL per
line, `#` comments and blank lines ignored), or both. A missing scheme is
assumed to be `https://`.

### Usage

```bash
# Check URLs given on the command line
python url_status_checker.py https://example.com https://google.com

# Check URLs from a file
python url_status_checker.py --file sample_urls.txt

# Also save results to CSV
python url_status_checker.py --file sample_urls.txt --output results.csv

# Tune concurrency and timeout
python url_status_checker.py --file urls.txt --workers 20 --timeout 10

# Full help
python url_status_checker.py --help
```

### Example

`python url_status_checker.py --file sample_urls.txt --output url_results.csv`:

```
Checked 6 URL(s): 4 OK, 2 failed/error
Saved: url_results.csv
```

`url_results.csv` contains the columns `url,status,final_url,time_s,error`.

---

## 3. domain_lookup.py — DNS domain checker

Checks whether 20 sample domain names resolve in DNS (via `socket`) and saves
the results to `domains_results.csv` with columns `domain, ip_address, status`.

### Usage

```bash
python3 domain_lookup.py
```

### Example

```
google.com                                    -> 142.250.x.x       RESOLVED
propakistani.pk                               -> 104.x.x.x          RESOLVED
this-domain-should-not-resolve-xyz123.com     -> -                  FAILED

18/20 domains resolved. Saved to domains_results.csv
```

(The two intentionally fake domains demonstrate FAILED handling.)

---

## 4. csv_merger.py — Merge CSVs, drop duplicates

Creates 3 sample customer CSVs (`samples/customers_a.csv` etc.), merges them
into `merged_customers.csv`, and removes exact duplicate rows (keeping the
first occurrence). Files with mismatched headers raise a clear error.

### Usage

```bash
python3 csv_merger.py
```

### Example

```
Sample files created:
  - samples/customers_a.csv
  - samples/customers_b.csv
  - samples/customers_c.csv

Rows read: 9 | Unique rows written: 7 | Duplicates removed: 2
Merged file: merged_customers.csv
```

---

## 5. file_renamer.py — Date-prefix file renamer

Renames every file in a folder to `YYYY-MM-DD_originalname`. Files that
already carry a date prefix are skipped; subdirectories are ignored.

### Usage

```bash
python3 file_renamer.py                 # demo on ./rename_demo
python3 file_renamer.py ./my_folder     # uses today's date
python3 file_renamer.py ./my_folder 2026-01-15   # custom date
```

### Example

```
report.pdf   -> 2026-10-08_report.pdf
notes.txt    -> 2026-10-08_notes.txt

Done: 2 file(s) renamed.
```

---

## 6. email_checker.py — Find invalid emails

Reads `emails.csv` (sample created on first run: 7 valid + 4 invalid
addresses), validates each address with a regex, prints the bad ones and
writes them to `invalid_emails.csv`.

### Usage

```bash
python3 email_checker.py
```

### Example

```
  INVALID: not-an-email (Bad Entry 1)
  INVALID: missing-at-sign.com (Bad Entry 2)
  INVALID: user@.com (Bad Entry 3)
  INVALID: double@@at.com (Bad Entry 4)

Checked emails.csv: 4 invalid address(es) written to invalid_emails.csv
```

---

## 7. csv_converter.py — CSV to JSON and Excel

Creates a sample `products.csv`, then converts it to `products.json` and
`products.xlsx` (bold header row, auto-sized columns) using `openpyxl`.

### Usage

```bash
python3 csv_converter.py
```

### Example

```
Read 5 rows from products.csv
Wrote products.json (5 records)
Wrote products.xlsx (5 rows)
```

---

## 8. receipt_generator.py — Incremental receipt numbers

Generates receipt numbers like `TAF-2026-0001`. The sequence persists in
`receipt_counter.txt`, so numbers keep increasing across runs. Pass a year
to use a different prefix year.

### Usage

```bash
python3 receipt_generator.py        # TAF-2026-0001
python3 receipt_generator.py        # TAF-2026-0002
python3 receipt_generator.py 2025   # TAF-2025-0003
```

---

## 9. test_scripts.py — pytest suite (10 tests)

Ten pytest tests covering `csv_merger.py` (dedup, header handling, empty
files, mismatch error) and `email_checker.py` (valid/invalid validation,
invalid-email export, whitespace handling).

### Usage

```bash
pytest test_scripts.py -v
# 10 passed
```

## 10. test_receipt_generator.py — pytest suite (5 tests)

Five pytest tests for the receipt generator: number format, incrementing
sequence, counter persistence, zero-padding (`TAF-2026-0042`), custom year.

### Usage

```bash
pytest test_receipt_generator.py -v
# 5 passed
```

---

## 11. donation_totals.py — Donation summary

Reads a mock `donations.csv` (8 sample donations) and prints the donation
count, total, average, and largest single gift.

### Usage

```bash
python3 donation_totals.py
```

### Example

```
Donations file : donations.csv
Donations count: 8
Total donated  : PKR 95,500
Average gift   : PKR 11,938
Largest gift   : PKR 25,000
```

---

## Running everything

```bash
cd techabout-python-tools
python3 -m venv venv && source venv/bin/activate
pip install openpyxl pytest
for s in domain_lookup csv_merger file_renamer email_checker csv_converter receipt_generator donation_totals; do
  echo "=== $s ==="; python3 $s.py
done
pytest -v
```

## Files

| File | Purpose |
|---|---|
| `csv_cleaner.py` | CSV cleaning CLI |
| `url_status_checker.py` | Concurrent URL status checker CLI |
| `domain_lookup.py` | DNS domain resolver → CSV |
| `csv_merger.py` | Merge CSVs, drop duplicates |
| `file_renamer.py` | Date-prefix file renamer |
| `email_checker.py` | Find invalid emails in CSV |
| `csv_converter.py` | CSV → JSON + Excel |
| `receipt_generator.py` | Incremental receipt numbers |
| `test_scripts.py` | 10 pytest tests (merger + email checker) |
| `test_receipt_generator.py` | 5 pytest tests (receipt generator) |
| `donation_totals.py` | Donation CSV summary |
| `SETUP_GUIDE.md` | Virtual-environment setup for new team members |
| `requirements.txt` | `openpyxl`, `pytest` |
