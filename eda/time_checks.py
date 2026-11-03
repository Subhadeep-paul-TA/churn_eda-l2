"""
Time-dimension diagnostics: the monthly transaction-volume trend (non-stationarity check),
and the multi-source agreement check between the row-level table and the pre-aggregated
monthly parquet extract.
"""

import pandas as pd


def monthly_volume_trend(transactions: pd.DataFrame) -> pd.DataFrame:
    """TODO: aggregate `transactions` to one row per calendar month with txn_count and
    total_amount, sorted chronologically, so the trend can be characterized (direction,
    rough magnitude) rather than asserted.
    """
    raise NotImplementedError


def compare_row_level_vs_monthly_agg(
    transactions: pd.DataFrame,
    monthly_agg: pd.DataFrame,
) -> pd.DataFrame:
    """TODO: reaggregate `transactions` to the same (customer_id, txn_month) grain as
    `monthly_agg`, join the two on (customer_id, txn_month), and return a per-month (or
    overall-by-month) comparison of txn_count and total_amount so any disagreement between
    the two sources is a number, not a guess. Do not assume they agree without checking.
    """
    raise NotImplementedError
