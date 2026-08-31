"""
reports.py
----------------
A handful of ready-made business reports run against the unified
sales warehouse, using plain SQL so they're easy to extend or port to
another database engine later.
"""

from database import query, TABLE_NAME


def total_sales_by_store() -> None:
    sql = f"""
        SELECT store_name,
               COUNT(DISTINCT transaction_id) AS num_transactions,
               SUM(quantity)                  AS total_units_sold,
               ROUND(SUM(total_amount), 2)    AS total_revenue
        FROM {TABLE_NAME}
        GROUP BY store_name
        ORDER BY total_revenue DESC;
    """
    print("\n=== Total Sales by Store ===")
    print(query(sql).to_string(index=False))


def top_selling_products(limit: int = 5) -> None:
    sql = f"""
        SELECT product_id, product_name,
               SUM(quantity)               AS total_units_sold,
               ROUND(SUM(total_amount), 2) AS total_revenue
        FROM {TABLE_NAME}
        GROUP BY product_id, product_name
        ORDER BY total_units_sold DESC
        LIMIT {limit};
    """
    print(f"\n=== Top {limit} Selling Products ===")
    print(query(sql).to_string(index=False))


def monthly_revenue_trend() -> None:
    sql = f"""
        SELECT sale_year, sale_month,
               ROUND(SUM(total_amount), 2) AS total_revenue
        FROM {TABLE_NAME}
        GROUP BY sale_year, sale_month
        ORDER BY sale_year, sale_month;
    """
    print("\n=== Monthly Revenue Trend ===")
    print(query(sql).to_string(index=False))


def sales_by_source_system() -> None:
    """Useful for data quality checks: how much volume came from each source."""
    sql = f"""
        SELECT source_system,
               COUNT(*)                    AS num_records,
               ROUND(SUM(total_amount), 2) AS total_revenue
        FROM {TABLE_NAME}
        GROUP BY source_system
        ORDER BY source_system;
    """
    print("\n=== Records by Source System (data quality check) ===")
    print(query(sql).to_string(index=False))


def run_all_reports() -> None:
    total_sales_by_store()
    top_selling_products()
    monthly_revenue_trend()
    sales_by_source_system()
