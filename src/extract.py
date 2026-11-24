import pandas as pd

REQUIRED_COLUMNS = ["order_id", "customer", "product", "quantity", "unit_price", "order_date"]


def extract_orders(csv_path):
    """Read the orders CSV and check that it has the required columns."""
    if not csv_path.exists():
        raise FileNotFoundError(f"input file not found: {csv_path}")

    try:
        orders = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        raise ValueError(f"input file is empty: {csv_path}")

    missing = [column for column in REQUIRED_COLUMNS if column not in orders.columns]
    if missing:
        raise ValueError(f"input file is missing columns: {', '.join(missing)}")

    return orders
