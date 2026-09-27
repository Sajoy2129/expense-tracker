# Expense Tracker

A simple terminal app for recording your expenses and seeing where your money goes.
Written in Python using only the standard library.

## Features

- **Add an expense** with a date, category, amount and optional note
- **List all expenses**, oldest first
- **Show totals per category**, plus a grand total
- **Show the total for a month** (for example `2026-09`)
- Data is saved automatically to `expenses.csv`, so it's still there next time

## Requirements

- Python 3.9 or newer
- [pytest](https://pytest.org), only if you want to run the tests

## Getting started

```bash
git clone https://github.com/Sajoy2129/expense-tracker.git
cd expense-tracker
python3 expenses.py
```

## Usage

```
=== Expense Tracker ===
1. Add an expense
2. List all expenses
3. Totals by category
4. Total for a month
5. Quit
Choose an option: 1
Date (YYYY-MM-DD, blank for today): 2026-09-03
Category: Food
Amount: 12.50
Note (optional): lunch, coffee
Added 12.50 for food on 2026-09-03.
```

Tips:
- Leave the date blank to use today's date.
- Categories are case-insensitive: `Food` and `food` count as the same category.
- If you type something invalid (like `abc` for an amount), the app explains the problem
  and asks again.

## Data file

Expenses are stored in `expenses.csv` in the folder you run the app from:

```csv
date,category,amount,note
2026-09-03,food,12.5,"lunch, coffee"
2026-08-20,food,40.0,groceries
```

You can open this file in Excel, Numbers or Google Sheets. It is listed in `.gitignore`,
so your personal spending data is never committed.

## Running the tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
pytest -v
```

## Project structure

```
expenses.py        # the app: file I/O, validation, logic, and the terminal menu
test_expenses.py   # pytest tests for the logic, validation and save/load
```
