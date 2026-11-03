"""
Test skeletons for eda/profile.py against small constructed DataFrames with a known shape,
so each profiling function's correctness doesn't depend on eyeballing the real dataset.

Fill these in against your confirmed eda_review.md and your actual profiling functions — do
not leave them skipped in your submission.
"""

import pytest


def test_profile_schema_reports_expected_columns_and_dtypes():
    """TODO: build a small DataFrame with known columns/dtypes and assert profile_schema
    reports them correctly."""
    pytest.skip("TODO: implement against eda/profile.py")


def test_profile_missingness_does_not_conflate_zero_activity_with_missing():
    """TODO: construct a customers frame and a transactions frame where some customers have
    zero matching rows, and assert count_zero_activity_customers reports them as
    zero-activity, not as a null value in some column."""
    pytest.skip("TODO: implement against eda/profile.py")


def test_profile_distribution_detects_right_skew():
    """TODO: construct a right-skewed series (e.g. mostly small values, one large outlier)
    and assert profile_distribution reports skew_direction == "right"."""
    pytest.skip("TODO: implement against eda/profile.py")


def test_count_outliers_flags_known_outlier():
    """TODO: construct a series with one deliberately extreme value and assert
    count_outliers flags exactly that value under the stated rule."""
    pytest.skip("TODO: implement against eda/profile.py")
