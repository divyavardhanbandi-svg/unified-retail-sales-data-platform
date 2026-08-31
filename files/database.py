"""
database.py
----------------
Loads the cleaned, unified sales DataFrame into a SQLite database
(acting as a lightweight "data warehouse" for this base project).

In a production setup you would point this at BigQuery, Snowflake,
Redshift, or a Postgres warehouse instead -- the rest of the pipeline
(ingestion, transform, reports) would not need to change.
"""

import sqlite3
import pandas as pd

DEFAULT_DB_PATH = "retail_platform.db"
TABLE_NAME = "unified_sales"


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    return sqlite3.connect(db_path)


def load_to_warehouse(df: pd.DataFrame, db_path: str = DEFAULT_DB_PATH,
                       if_exists: str = "replace") -> None:
    """
    Write the DataFrame to the SQLite warehouse table.
    if_exists: 'replace' (default, good for repeatable demo runs) or
               'append' (for incremental loads in a real pipeline).
    """
    conn = get_connection(db_path)
    try:
        df.to_sql(TABLE_NAME, conn, if_exists=if_exists, index=False)
        conn.commit()
        print(f"[database] Loaded {len(df)} rows into "
              f"'{TABLE_NAME}' table in {db_path}")
    finally:
        conn.close()


def query(sql: str, db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Run an arbitrary SQL query against the warehouse and return a DataFrame."""
    conn = get_connection(db_path)
    try:
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()
