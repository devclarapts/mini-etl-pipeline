import pandas as pd

from transform import transform_orders

COLUMNS = ["order_id", "customer", "product", "quantity", "unit_price", "order_date"]


def make_raw_orders(rows):
    return pd.DataFrame(rows, columns=COLUMNS)


def test_removes_duplicate_orders():
    raw = make_raw_orders([
        [1001, "Ana", "Mouse", 2, 45.5, "2024-03-01"],
        [1001, "Ana", "Mouse", 2, 45.5, "2024-03-01"],
        [1002, "Bruno", "Keyboard", 1, 120.0, "2024-03-02"],
    ])

    orders, stats = transform_orders(raw)

    assert stats["duplicates_removed"] == 1
    assert list(orders["order_id"]) == [1001, 1002]


def test_drops_rows_with_missing_values():
    raw = make_raw_orders([
        [1001, "Ana", "Mouse", 2, 45.5, "2024-03-01"],
        [1002, "", "Keyboard", 1, 120.0, "2024-03-02"],
        [1003, "Carla", "Monitor", None, 899.9, "2024-03-03"],
    ])

    orders, stats = transform_orders(raw)

    assert list(orders["order_id"]) == [1001]
    assert stats["invalid_removed"] == 2


def test_strips_whitespace_and_converts_types():
    raw = make_raw_orders([[1001, "  Ana  ", " Mouse ", "2", "45.5", "2024-03-01"]])

    orders, _ = transform_orders(raw)
    row = orders.iloc[0]

    assert row["customer"] == "Ana"
    assert row["product"] == "Mouse"
    assert row["quantity"] == 2
    assert row["unit_price"] == 45.5


def test_drops_rows_with_invalid_values():
    raw = make_raw_orders([
        [1001, "Ana", "Mouse", "two", 45.5, "2024-03-01"],
        [1002, "Bruno", "Keyboard", 1, -30.0, "2024-03-02"],
        [1003, "Carla", "Monitor", 1, 899.9, "not-a-date"],
        [1004, "Diego", "SSD", 0, 230.0, "2024-03-04"],
    ])

    orders, stats = transform_orders(raw)

    assert orders.empty
    assert stats["invalid_removed"] == 4


def test_standardizes_order_date():
    raw = make_raw_orders([[1001, "Ana", "Mouse", 1, 45.5, "2024/03/01"]])

    orders, _ = transform_orders(raw)

    assert orders.iloc[0]["order_date"] == "2024-03-01"


def test_stats_add_up():
    raw = make_raw_orders([
        [1001, "Ana", "Mouse", 2, 45.5, "2024-03-01"],
        [1001, "Ana", "Mouse", 2, 45.5, "2024-03-01"],
        [1002, "", "Keyboard", 1, 120.0, "2024-03-02"],
        [1003, "Carla", "Monitor", 1, 899.9, "2024-03-03"],
    ])

    orders, stats = transform_orders(raw)

    assert stats["source_rows"] == 4
    assert stats["duplicates_removed"] + stats["invalid_removed"] + stats["valid_rows"] == 4
    assert len(orders) == stats["valid_rows"]
