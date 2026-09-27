"""Tests for expenses.py. Run them with: pytest -v"""

import datetime

import pytest

import expenses as app


def make_expenses():
    """A small sample list shared by several tests."""
    return [
        {"date": "2026-09-01", "category": "food", "amount": 10.10, "note": ""},
        {"date": "2026-09-15", "category": "food", "amount": 0.20, "note": ""},
        {"date": "2026-09-20", "category": "transport", "amount": 5.00, "note": ""},
        {"date": "2026-10-02", "category": "food", "amount": 7.00, "note": ""},
        {"date": "2025-09-10", "category": "rent", "amount": 500.00, "note": ""},
    ]


# --- add_expense ---

def test_add_expense_appends_clean_dict():
    expenses = []
    app.add_expense(expenses, "2026-09-27", "  Food ", 12.5, " lunch ")
    assert expenses == [
        {"date": "2026-09-27", "category": "food", "amount": 12.5, "note": "lunch"}
    ]


# --- total_by_category ---

def test_total_by_category():
    totals = app.total_by_category(make_expenses())
    assert totals == {"food": 17.3, "transport": 5.0, "rent": 500.0}


def test_total_by_category_empty():
    assert app.total_by_category([]) == {}


# --- total_for_month ---

def test_total_for_month_only_counts_that_month():
    # 2025-09 rent must NOT be counted in 2026-09.
    assert app.total_for_month(make_expenses(), "2026-09") == 15.3


def test_total_for_month_with_no_matches():
    assert app.total_for_month(make_expenses(), "2030-01") == 0


# --- parsing / validation ---

@pytest.mark.parametrize("bad_text", ["abc", "-5", "0", "", "nan", "inf"])
def test_parse_amount_rejects_bad_input(bad_text):
    with pytest.raises(ValueError):
        app.parse_amount(bad_text)


def test_parse_amount_accepts_number():
    assert app.parse_amount("12.50") == 12.5


def test_parse_date_blank_means_today():
    assert app.parse_date("") == datetime.date.today().isoformat()


@pytest.mark.parametrize("bad_text", ["2026-13-01", "yesterday", "27/09/2026"])
def test_parse_date_rejects_bad_input(bad_text):
    with pytest.raises(ValueError):
        app.parse_date(bad_text)


def test_parse_month_accepts_valid_month():
    assert app.parse_month(" 2026-09 ") == "2026-09"


@pytest.mark.parametrize("bad_text", ["2026-13", "2026-9", "Sept", "2026-09-01"])
def test_parse_month_rejects_bad_input(bad_text):
    with pytest.raises(ValueError):
        app.parse_month(bad_text)
