"""
Runs eda/time_checks.py and eda/leakage_checks.py and prints/saves the results.

Run with `python -m scripts.run_time_and_leakage_checks`.

TODO:
- Run monthly_volume_trend and compare_row_level_vs_monthly_agg from eda/time_checks.py.
- Run flag_label_circular_drivers and check_no_post_as_of_rows_used from
  eda/leakage_checks.py, against the candidate drivers named in eda_review.md.
- Print a clear summary of the trend direction/magnitude, the multi-source gap (if any), and
  which drivers (if any) were flagged as leakage-tainted.
"""


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
