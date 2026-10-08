# Python Setup Guide (for new team members)

One page: get from zero to running these scripts in five minutes.

## 1. Install Python

- **Windows:** download the installer from python.org, tick
  "Add python.exe to PATH", install.
- **macOS:** `brew install python3` (or use the python.org installer).
- **Linux:** `sudo apt install python3 python3-venv python3-pip`

Check it works:

```bash
python3 --version   # need 3.8 or newer
```

## 2. Create a virtual environment

A virtual environment keeps project packages separate from system Python.

```bash
cd techabout-python-tools
python3 -m venv venv
```

## 3. Activate it

- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
- **macOS / Linux:** `source venv/bin/activate`

Your prompt now shows `(venv)` — that means it worked.

## 4. Install the needed packages

```bash
pip install openpyxl pytest
```

(`openpyxl` is only needed for the CSV-to-Excel script; `pytest` only for
running the test suites. Everything else uses the standard library.)

## 5. Run a script

```bash
python3 domain_lookup.py
python3 donation_totals.py
pytest -v          # run all tests
```

## 6. When you're done

```bash
deactivate
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `python3: command not found` | Use `python` instead, or reinstall with PATH enabled |
| `No module named 'openpyxl'` | Activate the venv first, then `pip install openpyxl` |
| Permission error on `pip install` | Never use `sudo pip` — use a venv |
| Tests fail on first run | Make sure you run `pytest` from the project folder |
