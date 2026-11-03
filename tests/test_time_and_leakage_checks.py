"""
Test skeletons for eda/time_checks.py and eda/leakage_checks.py against constructed input.

Fill these in against your confirmed eda_review.md and your actual functions — do not leave
them skipped in your submission.
"""

import pytest


def test_monthly_volume_trend_detects_growth():
    """TODO: construct a transactions frame with a clear month-over-month growth pattern and
    assert monthly_volume_trend reflects it (increasing txn_count/total_amount by month)."""
    pytest.skip("TODO: implement against eda/time_checks.py")


def test_compare_row_level_vs_monthly_agg_detects_known_mismatch():
    """TODO: construct a transactions frame and a monthly_agg frame that deliberately
    disagree for one month, and assert compare_row_level_vs_monthly_agg reports that
    month's discrepancy."""
    pytest.skip("TODO: implement against eda/time_checks.py")


def test_compare_row_level_vs_monthly_agg_confirms_agreement_when_consistent():
    """TODO: construct a transactions frame and a monthly_agg frame that agree everywhere,
    and assert the comparison reports no discrepancy — the check must not false-positive."""
    pytest.skip("TODO: implement against eda/time_checks.py")


def test_flag_label_circular_drivers_flags_trailing_window_features():
    """TODO: pass a candidate driver list including something like
    "days_since_last_txn" or "trailing_90d_spend" and assert
    flag_label_circular_drivers flags it, with a reason tied to the label's own
    trailing-90-day definition."""
    pytest.skip("TODO: implement against eda/leakage_checks.py")


def test_flag_label_circular_drivers_does_not_flag_legitimate_driver():
    """TODO: pass a candidate driver list including something like "tenure_days" (not
    definitionally tied to the label's trailing window) and assert it is NOT flagged —
    the check must not over-flag every strong result as leakage."""
    pytest.skip("TODO: implement against eda/leakage_checks.py")
