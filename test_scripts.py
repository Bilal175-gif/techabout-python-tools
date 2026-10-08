"""test_scripts.py — 10 pytest tests for csv_merger.py and email_checker.py.

Run with: pytest test_scripts.py -v
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import csv_merger
import email_checker


# ---------- csv_merger (5 tests) ----------

def _write_csv(path: Path, rows):
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)


def test_merge_removes_duplicates(tmp_path):
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    _write_csv(a, [["id", "name"], ["1", "Ahmed"], ["2", "Sara"]])
    _write_csv(b, [["id", "name"], ["2", "Sara"], ["3", "Usman"]])
    out = tmp_path / "out.csv"
    read, written = csv_merger.merge_csvs([a, b], out)
    assert read == 4
    assert written == 3  # one duplicate removed


def test_merge_keeps_header(tmp_path):
    a = tmp_path / "a.csv"
    _write_csv(a, [["id", "name"], ["1", "Ahmed"]])
    out = tmp_path / "out.csv"
    csv_merger.merge_csvs([a], out)
    with open(out, newline="") as f:
        header = next(csv.reader(f))
    assert header == ["id", "name"]


def test_merge_empty_second_file(tmp_path):
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    _write_csv(a, [["id"], ["1"], ["2"]])
    _write_csv(b, [["id"]])
    out = tmp_path / "out.csv"
    read, written = csv_merger.merge_csvs([a, b], out)
    assert (read, written) == (2, 2)


def test_merge_header_mismatch_raises(tmp_path):
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    _write_csv(a, [["id", "name"], ["1", "Ahmed"]])
    _write_csv(b, [["id", "city"], ["1", "Lahore"]])
    out = tmp_path / "out.csv"
    try:
        csv_merger.merge_csvs([a, b], out)
    except ValueError:
        return
    raise AssertionError("expected ValueError for header mismatch")


def test_merge_single_file_no_dedup_needed(tmp_path):
    a = tmp_path / "a.csv"
    _write_csv(a, [["id"], ["1"], ["2"], ["3"]])
    out = tmp_path / "out.csv"
    read, written = csv_merger.merge_csvs([a], out)
    assert (read, written) == (3, 3)


# ---------- email_checker (5 tests) ----------

def test_valid_emails_accepted():
    assert email_checker.is_valid("user@example.com")
    assert email_checker.is_valid("first.last@company.pk")
    assert email_checker.is_valid("name+tag@mail.co")


def test_invalid_emails_rejected():
    assert not email_checker.is_valid("not-an-email")
    assert not email_checker.is_valid("missing-at-sign.com")
    assert not email_checker.is_valid("user@.com")
    assert not email_checker.is_valid("double@@at.com")


def test_find_invalid_writes_output(tmp_path):
    src = tmp_path / "in.csv"
    dst = tmp_path / "out.csv"
    _write_csv(src, [["name", "email"],
                     ["Good", "good@example.com"],
                     ["Bad", "bad-email"]])
    invalid = email_checker.find_invalid(src, dst)
    assert len(invalid) == 1
    assert invalid[0]["email"] == "bad-email"
    assert dst.exists()


def test_all_valid_yields_empty_output(tmp_path):
    src = tmp_path / "in.csv"
    dst = tmp_path / "out.csv"
    _write_csv(src, [["name", "email"], ["A", "a@x.com"], ["B", "b@y.org"]])
    invalid = email_checker.find_invalid(src, dst)
    assert invalid == []


def test_whitespace_is_stripped():
    assert email_checker.is_valid("  user@example.com  ")
