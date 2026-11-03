"""
Test skeletons for eda/load.py's loaders against the real provided files.

Fill these in against your confirmed eda_review.md and your actual loader functions — do not
leave them skipped in your submission.
"""

import pytest


def test_load_customers_schema_and_row_count():
    """TODO: load customers.csv and assert expected columns, dtypes, and a sane row count."""
    pytest.skip("TODO: implement against eda/load.py")


def test_load_transactions_schema_and_row_count():
    """TODO: load transactions.db and assert expected columns, dtypes (txn_timestamp is a
    real datetime after loading, is_returned is 0/1 int), and a sane row count."""
    pytest.skip("TODO: implement against eda/load.py")


def test_load_monthly_agg_schema_and_row_count():
    """TODO: load transactions_monthly_agg.parquet and assert expected columns, dtypes, and
    a sane row count."""
    pytest.skip("TODO: implement against eda/load.py")
