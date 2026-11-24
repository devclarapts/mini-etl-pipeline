import sqlite3
from pathlib import Path

TABLE_NAME = "orders"


def load_orders(orders, db_path):
    """Write the orders to the SQLite database and return the stored row count."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect(db_path) as connection:
            orders.to_sql(TABLE_NAME, connection, if_exists="replace", index=False)
            cursor = connection.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            return cursor.fetchone()[0]
    except sqlite3.Error as error:
        raise RuntimeError(f"failed to write to {db_path}: {error}") from error
