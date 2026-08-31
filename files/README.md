# Unified Retail Sales Data Platform

A simple base project that solves a very common retail data problem:
sales data arrives from **multiple store systems**, each with its own
column names, layouts, and date formats. This platform ingests all of
them, maps them into **one unified schema**, cleans/enriches the data,
loads it into a warehouse, and runs business reports on top of it.

## Project Structure

```
unified_retail_platform/
├── generate_sample_data.py  # creates 3 sample CSVs simulating 3 different store systems
├── ingestion.py              # reads each source and maps it to a unified schema
├── transform.py               # cleans data + adds derived fields (total_amount, etc.)
├── database.py                # loads unified data into a SQLite warehouse
├── reports.py                  # business reports (SQL) run against the warehouse
├── main.py                     # orchestrates the full pipeline (CLI entry point)
├── requirements.txt
└── README.md
```

## The Problem This Solves

| | Store A (modern POS) | Store B (legacy) | Store C (legacy) |
|---|---|---|---|
| ID column | `TransactionID` | `txn_id` | `id` |
| Date column | `SaleDate` (`YYYY-MM-DD`) | `date` (`MM/DD/YYYY`) | `transaction_date` (`DD-MM-YYYY`) |
| Product | `SKU` / `ProductName` | `item_code` / `item_name` | `product_id` / `product_desc` |

Without unification, you can't run a single "total sales this month"
query across all stores. This pipeline maps every source into one
consistent schema:

```
transaction_id | sale_date | product_id | product_name |
quantity | unit_price | store_name | source_system |
total_amount | sale_year | sale_month
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

1. Generate sample multi-format data (skip this if you have your own CSVs):
   ```bash
   python generate_sample_data.py
   ```

2. Run the full pipeline (ingest -> clean -> load -> report):
   ```bash
   python main.py
   ```

   Or run the pipeline without printing reports:
   ```bash
   python main.py --no-reports
   ```

3. Explore the warehouse directly (it's just a SQLite file):
   ```bash
   sqlite3 retail_platform.db "SELECT * FROM unified_sales LIMIT 10;"
   ```

## Adding a New Store / Data Source

Open `ingestion.py` and add one new entry to `SOURCE_CONFIGS`:

```python
"store_d": {
    "file": "sample_data/store_d_sales.csv",
    "column_map": {
        "transaction_id": "OrderNo",
        "sale_date": "OrderDate",
        "product_id": "ItemNo",
        "product_name": "ItemDesc",
        "quantity": "Qty",
        "unit_price": "Price",
        "store_name": "Location",
    },
    "date_format": "%Y/%m/%d",
},
```

No other file needs to change — ingestion, transform, load, and reports
all work automatically against the unified schema.

## Included Reports

- **Total Sales by Store** — transactions, units sold, revenue per store
- **Top Selling Products** — best sellers by units and revenue
- **Monthly Revenue Trend** — revenue grouped by year/month
- **Records by Source System** — a basic data-quality check to see how
  much volume/revenue came from each source

## Possible Extensions

- Swap SQLite for a real cloud warehouse (**BigQuery**, **Redshift**,
  **Snowflake**, **Postgres**) — only `database.py` would need to change.
- Schedule the pipeline with **Airflow** or **cron** for daily/hourly loads.
- Add incremental loading (`if_exists="append"` in `database.py`) instead
  of a full replace each run.
- Build a dashboard on top of the warehouse with **Streamlit**, **Metabase**,
  or **Power BI**.
- Add data validation rules (e.g. with **Great Expectations**) before load.
- Containerize with Docker for consistent deployment.

## Java Note

This base project is implemented in Python (pandas + SQLite) since it's
the fastest way to prototype a unified data pipeline. The same
architecture — per-source config-driven mapping, a cleaning/enrichment
step, a warehouse load step, and a reporting layer — maps directly to
Java using **Apache Spark (Java API)** or plain JDBC + POJOs if you'd
like a Java implementation next; happy to build that version too.
