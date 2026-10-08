#!/usr/bin/env python3
"""file_renamer.py — Rename all files in a folder with a YYYY-MM-DD_ date prefix.

Example:
    report.pdf            -> 2026-10-08_report.pdf
    notes.txt             -> 2026-10-08_notes.txt

Files that already start with a date prefix are skipped. Subdirectories are
ignored. A rename log is printed and returned.

Usage:
    python3 file_renamer.py [folder] [date]
    python3 file_renamer.py ./my_folder            # uses today's date
    python3 file_renamer.py ./my_folder 2026-01-15  # uses a custom date
"""

import re
import sys
from datetime import date
from pathlib import Path

DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}_")


def rename_files(folder: Path, date_str: str) -> list[tuple[str, str]]:
    """Rename files in *folder* with a date prefix. Returns [(old, new)]."""
    renamed: list[tuple[str, str]] = []
    for entry in sorted(folder.iterdir()):
        if not entry.is_file():
            continue
        if DATE_PREFIX.match(entry.name):
            print(f"  skipped (already prefixed): {entry.name}")
            continue
        new_name = f"{date_str}_{entry.name}"
        entry.rename(entry.with_name(new_name))
        renamed.append((entry.name, new_name))
        print(f"  renamed: {entry.name} -> {new_name}")
    return renamed


def main() -> None:
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    date_str = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()

    if not folder.is_dir():
        print(f"Error: {folder} is not a directory")
        sys.exit(1)

    print(f"Renaming files in {folder} with prefix {date_str}_")
    renamed = rename_files(folder, date_str)
    print(f"\nDone: {len(renamed)} file(s) renamed.")


if __name__ == "__main__":
    # Demo: create a sample folder and rename its files
    demo = Path(__file__).with_name("rename_demo")
    demo.mkdir(exist_ok=True)
    for name in ("invoice.txt", "photo.png", "data.csv"):
        (demo / name).write_text("sample content\n")
    print("Demo folder contents before:", sorted(p.name for p in demo.iterdir()))
    renamed = rename_files(demo, date.today().isoformat())
    print("Demo folder contents after:", sorted(p.name for p in demo.iterdir()))
    print(f"\nUsage example: python3 file_renamer.py ./rename_demo")
