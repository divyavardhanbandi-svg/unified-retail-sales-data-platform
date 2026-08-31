"""
ingestion.py
----------------
Reads sales data exported by different store systems (each with its own
column names and date formats) and maps every source into ONE unified
schema:

    transaction_id | sale_date | product_id | product_name |
    quantity | unit_price | store_name | source_system

Adding a new store/source later just means adding one entry to
SOURCE_CONFIGS below -- no changes needed anywhere else in the pipeline.
"""

import pandas as pd

UNIFIED_COLUMNS = [
    "transaction_id", "sale_date", "product_id", "product_name",
    "quantity", "unit_price", "store_name", "source_system",
]

# Each source config maps: unified_column_name -> column_name_in_raw_file
# plus the date format used by that source.
SOURCE_CONFIGS = {
    "store_a": {
        "file": "sample_data/store_a_sales.csv",
        "column_map": {
            "transaction_id": "TransactionID",
            "sale_date": "SaleDate",
            "product_id": "SKU",
            "product_name": "ProductName",
            "quantity": "QtySold",
            "unit_price": "UnitPrice",
            "store_name": "StoreLocation",
        },
        "date_format": "%Y-%m-%d",
    },
    "store_b": {
        "file": "sample_data/store_b_sales.csv",
        "column_map": {
            "transaction_id": "txn_id",
            "sale_date": "date",
            "product_id": "item_code",
            "product_name": "item_name",
            "quantity": "quantity",
            "unit_price": "price_each",
            "store_name": "branch",
        },
        "date_format": "%m/%d/%Y",
    },
    "store_c": {
        "file": "sample_data/store_c_sales.csv",
        "column_map": {
            "transaction_id": "id",
            "sale_date": "transaction_date",
            "product_id": "product_id",
            "product_name": "product_desc",
            "quantity": "units",
            "unit_price": "price",
            "store_name": "outlet_name",
        },
        "date_format": "%d-%m-%Y",
    },
}


def _load_single_source(source_name: str, config: dict) -> pd.DataFrame:
    """Load one raw source file and rename/reformat it into the unified schema."""
    raw_df = pd.read_csv(config["file"])

    # Reverse the column_map so we can rename raw columns -> unified columns
    rename_map = {raw_col: unified_col
                  for unified_col, raw_col in config["column_map"].items()}
    df = raw_df.rename(columns=rename_map)

    # Keep only the columns we care about, in a consistent order
    df = df[list(config["column_map"].keys())]

    # Normalize the date column to a standard ISO format regardless of
    # how the source system originally formatted it.
    df["sale_date"] = pd.to_datetime(
        df["sale_date"], format=config["date_format"]
    ).dt.strftime("%Y-%m-%d")

    df["source_system"] = source_name
    return df


def load_all_sources(configs: dict = None) -> pd.DataFrame:
    """
    Load and unify every configured source into a single DataFrame with
    the UNIFIED_COLUMNS schema.
    """
    configs = configs or SOURCE_CONFIGS
    unified_frames = []

    for source_name, config in configs.items():
        print(f"[ingestion] Loading '{source_name}' from {config['file']}...")
        df = _load_single_source(source_name, config)
        print(f"[ingestion]   -> {len(df)} rows loaded")
        unified_frames.append(df)

    combined = pd.concat(unified_frames, ignore_index=True)
    combined = combined[UNIFIED_COLUMNS]
    print(f"[ingestion] Total unified rows: {len(combined)}")
    return combined
