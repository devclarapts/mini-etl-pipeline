from pathlib import Path

import pandas as pd
import pytest

from extract import extract_orders

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_extract_reads_project_csv():
    orders = extract_orders(PROJECT_ROOT / "data" / "orders.csv")

    assert list(orders.columns) == [
        "order_id",
        "customer",
        "product",
        "quantity",
        "unit_price",
        "order_date",
    ]
    assert len(orders) > 0


def test_extract_raises_when_file_is_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_orders(tmp_path / "missing.csv")


def test_extract_raises_when_columns_are_missing(tmp_path):
    csv_path = tmp_path / "bad.csv"
    pd.DataFrame({"order_id": [1], "customer": ["Ana"]}).to_csv(csv_path, index=False)

    with pytest.raises(ValueError):
        extract_orders(csv_path)


def test_extract_raises_when_file_is_empty(tmp_path):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("")

    with pytest.raises(ValueError):
        extract_orders(csv_path)
