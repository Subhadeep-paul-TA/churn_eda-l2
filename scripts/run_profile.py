"""
Runs eda/profile.py across all three sources and prints a human-readable summary.

Run with `python -m scripts.run_profile` (not `python scripts/run_profile.py`) so `eda`
resolves as an import.

TODO:
- Load all three sources via eda/load.py.
- Run profile_schema, profile_missingness, count_zero_activity_customers, and
  profile_distribution/count_outliers for every numeric column worth profiling per
  eda_review.md.
- Print a clear summary and (optionally) write it to outputs/artifacts/ for reference.
"""


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
