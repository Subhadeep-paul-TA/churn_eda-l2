"""
Test skeletons for each hypothesis function in eda/hypotheses.py, against constructed input
with a known answer.

Per skill.md's Workflow: each hypothesis function needs, at minimum, a case with a clear
engineered difference between groups (should come back significant) and a case with no real
difference (should come back non-significant, reported honestly, not omitted).

Fill these in against your confirmed eda_review.md and your actual hypothesis functions — do
not leave them skipped in your submission.
"""

import pytest


def test_hypothesis_detects_engineered_difference():
    """TODO: construct two groups with a clear, engineered difference and assert the
    relevant hypothesis function reports a significant result in the correct direction."""
    pytest.skip("TODO: implement against eda/hypotheses.py")


def test_hypothesis_reports_null_result_honestly():
    """TODO: construct two groups drawn from the same distribution (no real difference) and
    assert the relevant hypothesis function reports a non-significant result rather than a
    false positive."""
    pytest.skip("TODO: implement against eda/hypotheses.py")


def test_hypothesis_uses_test_matching_variable_shape():
    """TODO: for a driver eda_review.md designates as skewed/non-normal, assert the
    function actually uses a test appropriate to that shape (e.g. Mann-Whitney U), not a
    t-test applied without checking the normality assumption."""
    pytest.skip("TODO: implement against eda/hypotheses.py")
