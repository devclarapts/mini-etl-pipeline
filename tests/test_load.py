import sqlite3

import pandas as pd

from load import load_orders


def make_orders():
    return pd.DataFrame({
        "order_id": [1001, 1002],
        "customer": ["Ana", "Bruno"],
        "product": ["Mouse", "Keyboard"],
        "quantity": [2, 1],
        "unit_price": [45.5, 120.0],
        "order_date": ["2024-03-01", "2024-03-02"],
    })


def test_load_creates_database_and_returns_row_count(tmp_path):
    db_path = tmp_path / "database" / "orders.db"

    rows_loaded = load_orders(make_orders(), db_path)

    assert rows_loaded == 2
    assert db_path.exists()
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute("SELECT order_id FROM orders ORDER BY order_id").fetchall()
    assert rows == [(1001,), (1002,)]


def test_load_twice_does_not_duplicate_rows(tmp_path):
    db_path = tmp_path / "orders.db"

    load_orders(make_orders(), db_path)
    rows_loaded = load_orders(make_orders(), db_path)

    assert rows_loaded == 2


def test_load_raises_on_invalid_path():
    invalid_path = "Z:/path-that-does-not-exist/orders.db"

    try:
        load_orders(make_orders(), invalid_path)
        assert False, "expected RuntimeError"
    except (RuntimeError, OSError):
        pass
