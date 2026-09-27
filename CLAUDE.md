# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project
A Python expense tracker I'm building as a learning project: a terminal (menu-driven) app in a
single file, `expenses.py`. Standard library only; pytest is the only dev dependency.

## Commands
Run from the `expense_tracker/` directory (the data file path is relative — see below):
- Set up once: `python3 -m venv .venv && source .venv/bin/activate && pip install pytest`
- Run the app: `python3 expenses.py`
- All tests: `pytest -v`
- One test: `pytest test_expenses.py::test_total_for_month_only_counts_that_month`

## Architecture
`expenses.py` has four layers, top to bottom:
- **File I/O** — `load_expenses(path)` / `save_expenses(expenses, path)` read/write CSV with
  `csv.DictReader`/`DictWriter`. `path` defaults to `EXPENSES_FILE`; tests pass pytest's
  `tmp_path` instead, so they never touch real data.
- **Validation** — `parse_date`, `parse_amount`, `parse_month` turn raw text into clean values or
  raise `ValueError` with a user-friendly message. No `input()`/`print()` here.
- **Logic** — `add_expense` (mutates the list in place), `total_by_category`, `total_for_month`.
  Pure and tested directly.
- **Terminal I/O** — `show_expenses`, `show_category_totals`, `ask(prompt, parser)` (re-prompts
  until the parser stops raising), and `main()`.

Conventions:
- Data model: list of dicts `{"date": "YYYY-MM-DD", "category": str (lowercase), "amount": float,
  "note": str}`. Amounts are text in the CSV; `load_expenses` converts them back to float.
- Month matching is `date.startswith("YYYY-MM-")` — relies on ISO date strings.
- Totals are rounded to 2 decimals to hide float noise.
- `main()` loads once at startup and calls `save_expenses()` after every change.
- `expenses.csv` is user data and is gitignored. It lives in the current working directory.
