"""
Leakage-discipline checks specific to this dataset's label definition: churn = no purchase
in the 90 days before the as-of date.

A feature computed over a window that overlaps that same trailing period is not merely
correlated with the label — it is circular with it. These checks exist to catch that
specifically, not to raise a generic "be careful about leakage" warning.
"""

import pandas as pd


def flag_label_circular_drivers(candidate_drivers: list[str]) -> dict:
    """TODO: given the list of candidate driver names in eda_review.md, return which of
    them (if any) are computed over a window that overlaps the label's own trailing-90-day
    definition (e.g. days-since-last-transaction, trailing-90-day spend), with a one-line
    reason per flagged driver. Do not flag a driver that is merely correlated but not
    definitionally derived from the same window (e.g. account tenure).
    """
    raise NotImplementedError


def check_no_post_as_of_rows_used(transactions: pd.DataFrame, as_of: str) -> dict:
    """TODO: confirm no row in `transactions` with txn_timestamp after `as_of` was used in
    any profiling or hypothesis-test computation. Return {"passed": bool, "n_post_as_of_rows
    _in_source": int, "note": str} — the source file may contain rows after as_of (it is not
    edited), the check is that your OWN computations excluded them.
    """
    raise NotImplementedError
