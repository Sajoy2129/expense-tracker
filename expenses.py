"""A simple terminal expense tracker. Expenses are saved in expenses.csv."""

import csv
import datetime
import math
import os

EXPENSES_FILE = "expenses.csv"
FIELDS = ["date", "category", "amount", "note"]


# --- File I/O: the path is a parameter so tests can use a temporary file ---

def load_expenses(path=EXPENSES_FILE):
    """Read expenses from the CSV file. Return an empty list if there's no file yet."""
    if not os.path.exists(path):
        return []
    with open(path, newline="") as file:
        expenses = list(csv.DictReader(file))
    # CSV stores everything as text, so turn amounts back into numbers.
    for expense in expenses:
        expense["amount"] = float(expense["amount"])
    return expenses


def save_expenses(expenses, path=EXPENSES_FILE):
    """Write all expenses to the CSV file, with a header row."""
    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


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


# --- Terminal I/O: printing and asking questions ---

def show_expenses(expenses):
    """Print every expense as a table, oldest first."""
    if not expenses:
        print("No expenses yet.")
        return
    print(f"{'Date':<12}{'Category':<15}{'Amount':>10}  Note")
    for expense in sorted(expenses, key=lambda e: e["date"]):
        print(
            f"{expense['date']:<12}{expense['category']:<15}"
            f"{expense['amount']:>10.2f}  {expense['note']}"
        )


def show_category_totals(expenses):
    """Print the total for each category, plus a grand total."""
    totals = total_by_category(expenses)
    if not totals:
        print("No expenses yet.")
        return
    for category, total in sorted(totals.items()):
        print(f"{category:<15}{total:>10.2f}")
    print(f"{'TOTAL':<15}{sum(totals.values()):>10.2f}")


def ask(prompt, parser):
    """Keep asking until `parser` accepts the answer, then return the parsed value."""
    while True:
        try:
            return parser(input(prompt))
        except ValueError as error:
            print(error)


def main():
    expenses = load_expenses()

    while True:
        print()
        print("=== Expense Tracker ===")
        print("1. Add an expense")
        print("2. List all expenses")
        print("3. Totals by category")
        print("4. Total for a month")
        print("5. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            date = ask("Date (YYYY-MM-DD, blank for today): ", parse_date)
            category = input("Category: ").strip()
            if not category:
                print("The category can't be empty.")
                continue
            amount = ask("Amount: ", parse_amount)
            note = input("Note (optional): ")
            add_expense(expenses, date, category, amount, note)
            save_expenses(expenses)
            print(f"Added {amount:.2f} for {category.lower()} on {date}.")
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_category_totals(expenses)
        elif choice == "4":
            month = ask("Month (YYYY-MM): ", parse_month)
            print(f"Total for {month}: {total_for_month(expenses, month):.2f}")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3, 4 or 5.")


# Only run the app when this file is run directly (not when tests import it).
if __name__ == "__main__":
    main()
