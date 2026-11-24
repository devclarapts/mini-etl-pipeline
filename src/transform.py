import pandas as pd

TEXT_COLUMNS = ["customer", "product"]
REQUIRED_COLUMNS = ["order_id", "customer", "product", "quantity", "unit_price", "order_date"]


def transform_orders(raw_orders):
    """Clean the raw orders and return the valid rows with pipeline stats."""
    orders = raw_orders.copy()
    source_rows = len(orders)

    for column in TEXT_COLUMNS:
        orders[column] = orders[column].astype("string").str.strip()

    orders["quantity"] = pd.to_numeric(orders["quantity"], errors="coerce")
    orders["unit_price"] = pd.to_numeric(orders["unit_price"], errors="coerce")
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce", format="mixed")

    orders = orders.drop_duplicates(subset="order_id", keep="first")
    duplicates_removed = source_rows - len(orders)

    orders = orders[is_valid(orders)]
    invalid_removed = source_rows - duplicates_removed - len(orders)

    orders = orders.reset_index(drop=True)
    orders["quantity"] = orders["quantity"].astype(int)
    orders["unit_price"] = orders["unit_price"].round(2)
    orders["order_date"] = orders["order_date"].dt.strftime("%Y-%m-%d")

    stats = {
        "source_rows": source_rows,
        "duplicates_removed": duplicates_removed,
        "invalid_removed": invalid_removed,
        "valid_rows": len(orders),
    }
    return orders, stats


def is_valid(orders):
    """Return a boolean mask with the business rules each row must satisfy."""
    has_required_fields = orders[REQUIRED_COLUMNS].notna().all(axis=1)
    has_text = orders["customer"].ne("") & orders["product"].ne("")
    valid_quantity = orders["quantity"] >= 1
    valid_price = orders["unit_price"] > 0
    return has_required_fields & has_text & valid_quantity & valid_price
