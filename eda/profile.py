"""
Schema, missingness, distribution-shape, and outlier profiling for the three raw sources.

Every function here should return something concrete an evaluator (or
`scripts/verify_findings.py`) can check against the real data — not a prose-only summary.
"""

import pandas as pd


def profile_schema(df: pd.DataFrame) -> dict:
    """TODO: return {"columns": [...], "dtypes": {...}, "n_rows": int} for the given frame."""
    raise NotImplementedError


def profile_missingness(df: pd.DataFrame) -> dict:
    """TODO: return per-column null counts.

    Do not conflate a customer legitimately absent from transactions.db (zero activity) with
    an actually-missing value in a column that IS present — see `count_zero_activity_customers`
    below for the former.
    """
    raise NotImplementedError


def count_zero_activity_customers(customers: pd.DataFrame, transactions: pd.DataFrame) -> int:
    """TODO: count customers with zero matching rows in `transactions`. Compute this
    directly — do not hardcode a number from any prior document."""
    raise NotImplementedError


def profile_distribution(series: pd.Series) -> dict:
    """TODO: return at minimum {"mean": ..., "median": ..., "skew_direction": "left"/"right"/
    "roughly symmetric", "min": ..., "max": ...} for a numeric column. Use the gap between
    mean and median (or a skewness statistic) to decide the skew direction — do not eyeball it.
    """
    raise NotImplementedError


def count_outliers(series: pd.Series, rule: str = "iqr", multiplier: float = 1.5) -> dict:
    """TODO: return {"rule": rule, "bound_low": ..., "bound_high": ..., "n_outliers": ...}
    using an explicit, stated rule (e.g. values outside [Q1 - multiplier*IQR, Q3 +
    multiplier*IQR]) — never just "eyeballed as an outlier."
    """
    raise NotImplementedError
