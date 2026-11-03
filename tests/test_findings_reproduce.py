"""
The test that matters most for this assignment: proves every numeric claim stated in
EDA_FINDINGS.md actually reproduces from the raw data, rather than being merely asserted in
prose.

This mirrors the role test_parity.py plays in the companion feature-pipeline assignment —
except here the guarantee being tested is "every stated finding is real," not "training and
scoring agree."

Fill this in once EDA_FINDINGS.md exists, against the actual claims it makes — do not leave
it skipped in your submission.
"""

import pytest


def test_churn_rate_claim_reproduces():
    """TODO: recompute the overall churn rate from data/customers.csv and assert it matches
    the number stated in EDA_FINDINGS.md."""
    pytest.skip("TODO: implement once EDA_FINDINGS.md exists")


def test_zero_activity_count_claim_reproduces():
    """TODO: recompute the zero-activity customer count and assert it matches the number
    stated in EDA_FINDINGS.md."""
    pytest.skip("TODO: implement once EDA_FINDINGS.md exists")


def test_each_hypothesis_result_reproduces():
    """TODO: for every hypothesis test claim in EDA_FINDINGS.md, recompute it via
    eda/hypotheses.py and assert the statistic/p-value/direction match within a sane
    tolerance."""
    pytest.skip("TODO: implement once EDA_FINDINGS.md exists")


def test_multi_source_gap_claim_reproduces():
    """TODO: recompute the row-level-vs-monthly-agg comparison via eda/time_checks.py and
    assert it matches what EDA_FINDINGS.md states about where/how much the two sources
    disagree."""
    pytest.skip("TODO: implement once EDA_FINDINGS.md exists")
