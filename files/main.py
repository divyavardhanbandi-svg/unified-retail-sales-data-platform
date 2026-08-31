"""
main.py
----------------
Orchestrates the full Unified Retail Sales Data Platform pipeline:

    1. INGEST  -> read sales exports from multiple store systems
                  (each with different column names / date formats)
    2. TRANSFORM -> clean the data and compute derived fields
    3. LOAD     -> write the unified data into a SQLite warehouse
    4. REPORT   -> run business reports against the warehouse

Usage:
    python main.py              # run full pipeline + reports
    python main.py --no-reports # run pipeline only, skip printing reports
"""

import argparse

from ingestion import load_all_sources
from transform import run_pipeline
from database import load_to_warehouse
from reports import run_all_reports


def run(skip_reports: bool = False) -> None:
    print("=" * 60)
    print("UNIFIED RETAIL SALES DATA PLATFORM")
    print("=" * 60)

    # 1. Ingest data from every configured store source
    raw_unified_df = load_all_sources()

    # 2. Clean + enrich the data
    clean_df = run_pipeline(raw_unified_df)

    # 3. Load into the warehouse (SQLite for this base project)
    load_to_warehouse(clean_df)

    # 4. Run business reports
    if not skip_reports:
        run_all_reports()

    print("\nPipeline completed successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Run the Unified Retail Sales Data Platform pipeline."
    )
    parser.add_argument("--no-reports", action="store_true",
                        help="Run ingestion/transform/load only, skip reports")
    args = parser.parse_args()
    run(skip_reports=args.no_reports)


if __name__ == "__main__":
    main()
