"""
Reproduces every numeric claim stated in EDA_FINDINGS.md directly from the raw data sources,
and fails loudly (non-zero exit) if any recomputed value doesn't match what's stated.

This is the parity-test equivalent for this assignment: EDA_FINDINGS.md is only trustworthy
if every number in it can be regenerated from code against the real data, not merely
asserted in prose.

Run with `python -m scripts.verify_findings`.

TODO:
- For each numeric claim in EDA_FINDINGS.md (churn rate, zero-activity count, each
  hypothesis test's statistic/p-value, the monthly trend direction/magnitude, the
  multi-source gap), recompute it using eda/profile.py, eda/hypotheses.py, and
  eda/time_checks.py.
- Compare each recomputed value against the stated value within a sane tolerance.
- Print a pass/fail per claim and exit non-zero if anything doesn't match.
"""


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
