"""
One pure function per candidate churn-driver named in your confirmed `eda_review.md`.

Each function should:
- Take already-loaded/derived data in (no I/O here) and return a structured result out:
  {"driver": str, "test": str, "statistic": float, "p_value": float,
   "effect_size_or_magnitude": ..., "higher_group": "churned"/"not_churned"/None}.
- Choose the test that matches the variable's actual shape per eda_review.md (chi-square for
  a categorical driver, Mann-Whitney U for a skewed/non-normal continuous driver, a t-test
  only after checking the normality assumption actually holds) — do not default to a t-test
  for everything.
- Report the result honestly even when it is not statistically significant. A null result is
  a real finding, not a failure to report.

This file intentionally contains no implementations. Add one function per driver as you
build against your confirmed eda_review.md.
"""

import pandas as pd


def example_hypothesis_placeholder(
    customers: pd.DataFrame,
    driver_values: pd.Series,
) -> dict:
    """TODO: replace with your first real hypothesis test function.

    Rename this function (and this file's contents) to match the candidate drivers named in
    your confirmed eda_review.md. Keep one function per driver.
    """
    raise NotImplementedError
