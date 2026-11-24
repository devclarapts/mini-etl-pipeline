# Mini ETL Pipeline

A small ETL (Extract, Transform, Load) pipeline that reads store order data from a CSV file, cleans it with pandas, and loads the valid records into a SQLite database.

The input file intentionally contains common data quality problems (duplicates, missing fields, extra whitespace, invalid values) so the cleaning steps have real work to do.

## Objective

Practice the core stages of a data pipeline in a single, readable project:

- Extract data from a flat file with basic validation.
- Apply cleaning and type conversion rules.
- Load the result into a database in an idempotent way.
- Report what happened to the data at each stage.

## Technologies

- Python 3.10+
- pandas
- SQLite (standard library `sqlite3`)
- pytest

## Project structure

```
mini-etl-pipeline/
├── data/
│   └── orders.csv          # raw input with intentional data problems
├── database/               # orders.db is created here at runtime
├── src/
│   ├── main.py             # runs the pipeline and prints the report
│   ├── extract.py          # CSV reading and input validation
│   ├── transform.py        # cleaning, type conversion, business rules
│   └── load.py             # SQLite writing
├── tests/
│   ├── conftest.py
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── requirements.txt
└── README.md
```

## ETL workflow

1. **Extract** — `extract.py` checks that `data/orders.csv` exists, is not empty, and contains the required columns (`order_id`, `customer`, `product`, `quantity`, `unit_price`, `order_date`). Any problem raises an error and the pipeline stops.
2. **Transform** — `transform.py` trims whitespace from text fields, converts `quantity` and `unit_price` to numbers and `order_date` to dates (invalid values become missing), removes duplicate `order_id` entries keeping the first occurrence, and drops rows that fail validation: missing required fields, empty customer or product, quantity below 1, or non-positive price. Dates are standardized to `YYYY-MM-DD`.
3. **Load** — `load.py` writes the result to the `orders` table in `database/orders.db` using `if_exists="replace"`, so re-running the pipeline never duplicates data. The stored row count is read back from the database and compared against the transformation stats; a mismatch is treated as a failure.

## Installation

```bash
git clone <repository-url>
cd mini-etl-pipeline
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

## How to run

```bash
python src/main.py
```

To run the tests:

```bash
python -m pytest tests -v
```

## Example output

```
ETL pipeline finished
Records in source:    22
Duplicates removed:   2
Invalid records:      10
Valid records:        10
Records in database:  10
```

## Future improvements

- Log to a file instead of printing to the console.
- Archive rejected rows in a separate table for inspection.
- Incremental loads with `INSERT OR IGNORE` instead of replacing the whole table.
- Accept the input path as a command-line argument.
