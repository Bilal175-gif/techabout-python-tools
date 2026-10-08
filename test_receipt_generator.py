"""test_receipt_generator.py — 5 pytest tests for receipt_generator.py.

Run with: pytest test_receipt_generator.py -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import receipt_generator


def test_format_matches_pattern(tmp_path, monkeypatch):
    monkeypatch.setattr(receipt_generator, "COUNTER_FILE", tmp_path / "c.txt")
    receipt = receipt_generator.next_receipt("2026")
    assert receipt.startswith("TAF-2026-")
    assert len(receipt) == len("TAF-2026-0001")


def test_counter_increments(tmp_path, monkeypatch):
    monkeypatch.setattr(receipt_generator, "COUNTER_FILE", tmp_path / "c.txt")
    first = receipt_generator.next_receipt("2026")
    second = receipt_generator.next_receipt("2026")
    assert first == "TAF-2026-0001"
    assert second == "TAF-2026-0002"


def test_counter_persists_across_reads(tmp_path, monkeypatch):
    monkeypatch.setattr(receipt_generator, "COUNTER_FILE", tmp_path / "c.txt")
    receipt_generator.next_receipt("2026")
    receipt_generator.next_receipt("2026")
    assert receipt_generator.read_counter() == 2


def test_zero_padded_sequence(tmp_path, monkeypatch):
    monkeypatch.setattr(receipt_generator, "COUNTER_FILE", tmp_path / "c.txt")
    (tmp_path / "c.txt").write_text("41")
    assert receipt_generator.next_receipt("2026") == "TAF-2026-0042"


def test_custom_year(tmp_path, monkeypatch):
    monkeypatch.setattr(receipt_generator, "COUNTER_FILE", tmp_path / "c.txt")
    assert receipt_generator.next_receipt("2025") == "TAF-2025-0001"
