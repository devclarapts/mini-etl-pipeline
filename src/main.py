import sys
from pathlib import Path

from extract import extract_orders
from load import load_orders
from transform import transform_orders

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "orders.csv"
DB_PATH = PROJECT_ROOT / "database" / "orders.db"


def main():
    try:
        raw_orders = extract_orders(CSV_PATH)
        clean_orders, stats = transform_orders(raw_orders)
        rows_loaded = load_orders(clean_orders, DB_PATH)
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"Pipeline failed: {error}")
        return 1

    if rows_loaded != stats["valid_rows"]:
        print("Pipeline failed: row count in database does not match valid records")
        return 1

    print("ETL pipeline finished")
    print(f"Records in source:    {stats['source_rows']}")
    print(f"Duplicates removed:   {stats['duplicates_removed']}")
    print(f"Invalid records:      {stats['invalid_removed']}")
    print(f"Valid records:        {stats['valid_rows']}")
    print(f"Records in database:  {rows_loaded}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
