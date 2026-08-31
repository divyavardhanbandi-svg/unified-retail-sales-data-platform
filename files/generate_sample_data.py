"""
generate_sample_data.py
----------------
Creates three CSV files that simulate sales exports from three different
retail store systems, each with its OWN column names, layouts and date
formats. This mimics the real-world problem this platform solves: making
sense of sales data coming from different POS systems before it can be
analyzed together.

Run this once before running the pipeline if you don't have your own data:
    python generate_sample_data.py
"""

import csv
import os
import random
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_data")

PRODUCTS = [
    ("SKU001", "Wireless Mouse", 19.99),
    ("SKU002", "Bluetooth Speaker", 45.50),
    ("SKU003", "USB-C Cable", 9.99),
    ("SKU004", "Laptop Stand", 32.00),
    ("SKU005", "Mechanical Keyboard", 79.99),
    ("SKU006", "Webcam HD", 55.25),
]

random.seed(42)


def random_date(days_back=30):
    return datetime.now() - timedelta(days=random.randint(0, days_back))


def generate_store_a(path, num_rows=40):
    """Store A: modern POS export -- clean column names, ISO dates."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TransactionID", "SaleDate", "SKU", "ProductName",
                          "QtySold", "UnitPrice", "StoreLocation"])
        for i in range(num_rows):
            sku, name, price = random.choice(PRODUCTS)
            writer.writerow([
                f"A-{1000 + i}",
                random_date().strftime("%Y-%m-%d"),
                sku, name,
                random.randint(1, 5),
                price,
                "Downtown Store",
            ])


def generate_store_b(path, num_rows=35):
    """Store B: legacy system -- abbreviated columns, US date format."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["txn_id", "date", "item_code", "item_name",
                          "quantity", "price_each", "branch"])
        for i in range(num_rows):
            sku, name, price = random.choice(PRODUCTS)
            writer.writerow([
                f"B-{2000 + i}",
                random_date().strftime("%m/%d/%Y"),
                sku, name,
                random.randint(1, 5),
                price,
                "Mall Branch",
            ])


def generate_store_c(path, num_rows=30):
    """Store C: another legacy system -- different naming, dd-mm-yyyy dates."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "transaction_date", "product_id",
                          "product_desc", "units", "price", "outlet_name"])
        for i in range(num_rows):
            sku, name, price = random.choice(PRODUCTS)
            writer.writerow([
                f"C-{3000 + i}",
                random_date().strftime("%d-%m-%Y"),
                sku, name,
                random.randint(1, 5),
                price,
                "Airport Outlet",
            ])


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generate_store_a(os.path.join(OUTPUT_DIR, "store_a_sales.csv"))
    generate_store_b(os.path.join(OUTPUT_DIR, "store_b_sales.csv"))
    generate_store_c(os.path.join(OUTPUT_DIR, "store_c_sales.csv"))
    print(f"Sample data generated in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
