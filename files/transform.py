"""
transform.py
----------------
Cleans and enriches the unified sales DataFrame before it's loaded into
the warehouse:
  - drops duplicate/invalid rows
  - fills or flags missing values
  - computes derived fields (total_amount, sale_year, sale_month)
"""

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)

    # Drop exact duplicate transactions (can happen with repeated exports)
    df = df.drop_duplicates(subset=["transaction_id", "source_system"])

    # Drop rows missing critical fields
    df = df.dropna(subset=["product_id", "quantity", "unit_price", "sale_date"])

    # Ensure numeric types are correct; coerce bad values to NaN then drop them
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["quantity", "unit_price"])

    # Remove nonsensical values (e.g. negative price/quantity from bad exports)
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]

    after = len(df)
    print(f"[transform] Cleaned data: {before} -> {after} rows "
          f"({before - after} removed)")
    return df


def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["total_amount"] = (df["quantity"] * df["unit_price"]).round(2)

    sale_dates = pd.to_datetime(df["sale_date"])
    df["sale_year"] = sale_dates.dt.year
    df["sale_month"] = sale_dates.dt.month

    print("[transform] Enriched data with total_amount, sale_year, sale_month")
    return df


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_data(df)
    df = enrich_data(df)
    return df
