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


# --- saving and loading (tmp_path is a temporary folder pytest gives us) ---

def test_save_then_load_gives_same_expenses(tmp_path):
    path = tmp_path / "expenses.csv"
    expenses = make_expenses()
    # A comma inside a note must not split the row into extra columns.
    expenses[0]["note"] = "lunch, coffee"
    app.save_expenses(expenses, path)
    assert app.load_expenses(path) == expenses


def test_load_missing_file_returns_empty_list(tmp_path):
    assert app.load_expenses(tmp_path / "nope.csv") == []


def test_load_skips_broken_rows(tmp_path, capsys):
    # Rows a person might create by editing the file by hand.
    path = tmp_path / "expenses.csv"
    path.write_text(
        "date,category,amount,note\n"
        "2026-09-01,food,12.5,good row\n"
        "2026-09-02,food,,blank amount\n"
        "2026-09-03,food,abc,not a number\n"
        "2026-09-04,food,nan,not a real number\n"
        "2026-09-05,food\n"
        "2026-09-06,transport,3,another good row\n"
    )
    expenses = app.load_expenses(path)
    assert [e["note"] for e in expenses] == ["good row", "another good row"]
    # capsys captures what was printed, so we can check the warnings.
    warnings = capsys.readouterr().out
    for line_number in [3, 4, 5, 6]:
        assert f"line {line_number}" in warnings


def test_failed_save_keeps_old_file(tmp_path, monkeypatch):
    path = tmp_path / "expenses.csv"
    app.save_expenses(make_expenses(), path)

    # Pretend the program crashes halfway through writing the rows.
    def crash(self, rows):
        raise OSError("disk full")
    monkeypatch.setattr(app.csv.DictWriter, "writerows", crash)

    with pytest.raises(OSError):
        app.save_expenses([], path)
    # The old data must still be there, not an empty file.
    assert app.load_expenses(path) == make_expenses()


@pytest.mark.parametrize("error", [KeyboardInterrupt, EOFError])
def test_ctrl_c_and_ctrl_d_quit_cleanly(error, tmp_path, monkeypatch, capsys):
    # Run in a temp folder so the app never touches the real expenses.csv.
    monkeypatch.chdir(tmp_path)

    def fake_input(prompt):
        raise error
    monkeypatch.setattr("builtins.input", fake_input)

    app.main()  # must not raise
    assert "Goodbye!" in capsys.readouterr().out
