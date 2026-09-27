"""A simple terminal expense tracker. Expenses are saved in expenses.csv."""

import datetime
import math


# --- Validation: turn user text into clean values, or raise ValueError ---

def parse_date(text):
    """Return a YYYY-MM-DD date string. Blank text means today."""
    text = text.strip()
    if not text:
        return datetime.date.today().isoformat()
    try:
        return datetime.date.fromisoformat(text).isoformat()
    except ValueError:
        raise ValueError("Please enter a date like 2026-09-27.")


def parse_amount(text):
    """Return the amount as a float. It must be a number greater than 0."""
    try:
        amount = float(text)
    except ValueError:
        raise ValueError("Please enter a number, like 12.50.")
    # float() also accepts "nan" and "inf", which would break every total.
    if not math.isfinite(amount):
        raise ValueError("Please enter a number, like 12.50.")
    if amount <= 0:
        raise ValueError("The amount must be greater than 0.")
    return amount


def parse_month(text):
    """Return a YYYY-MM month string."""
    text = text.strip()
    try:
        # Adding "-01" turns a month into a real date we can check.
        datetime.date.fromisoformat(text + "-01")
    except ValueError:
        raise ValueError("Please enter a month like 2026-09.")
    if len(text) != 7:
        raise ValueError("Please enter a month like 2026-09.")
    return text


# --- Logic: work on the list of expenses (no input/print) ---

def add_expense(expenses, date, category, amount, note):
    """Add a new expense. Categories are stored lowercase."""
    expenses.append({
        "date": date,
        "category": category.strip().lower(),
        "amount": amount,
        "note": note.strip(),
    })


def total_by_category(expenses):
    """Return a dict like {"food": 42.5, "transport": 10.0}."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    # Round to cents so float errors like 0.30000000000000004 disappear.
    return {category: round(total, 2) for category, total in totals.items()}


def total_for_month(expenses, month):
    """Return the total spent in `month` (a "YYYY-MM" string)."""
    total = sum(
        expense["amount"]
        for expense in expenses
        if expense["date"].startswith(month + "-")
    )
    return round(total, 2)
