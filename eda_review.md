# eda_review.md — Churn EDA & Model-Family Recommendation

## Distribution / missingness / outlier corrections

- **Correction**: Stage 0's draft called `transactions.amount` "roughly normal" in the
  model recommendation draft — checked mean ($49.72) vs. median ($33.82); skew is 6.11
  and the max is $1,684.21 against a 75th-percentile of $125.93. This is strongly
  right-skewed with a long high-value tail, not normal. Any downstream summary stat for
  monetary features should use median/IQR rather than mean/std.

- **Correction**: Stage 0's draft flagged the 1.5×IQR rule on the raw scale as the
  outlier threshold, calling 783 transactions (6.7%) above $125.93 outliers. Applying
  the same 1.5×IQR rule on the log scale flags only 86 transactions. The choice of
  scale materially changes what gets flagged, and neither is obviously correct — the
  build stage must pick and document a rule rather than leaving it open.

- **Correction**: Stage 0's draft notes 81 customers with no transaction rows as "5.4%
  with zero rows in transactions.db." The draft itself uses the right language in one
  place, but the model-recommendation draft slides into treating them as missing data.
  They are not missing: they legitimately transacted zero times and are labelled
  `churned = 1`. All 81 are churned, making up 40.1% (81 of 202) of all churners.
  Every transaction-derived ratio feature is undefined for them; they should not be
  treated as imputable missingness.

## Hypothesis tests to run

- **Driver**: `acquisition_channel`
- **Test**: chi-square
- **Why this test**: 4-level categorical predictor vs. binary churn outcome; no ordering
  assumption. Overall churn by channel ranges from 10.2% (paid_search) to 15.3%
  (organic), a gap worth testing.

- **Driver**: `region`
- **Test**: chi-square
- **Why this test**: 4-level unordered categorical vs. binary churn; east is highest at
  16.4% vs. 12.3%–12.7% for the other three regions.

- **Driver**: `txn_per_30d_tenure` (purchase rate normalised by tenure)
- **Test**: Mann-Whitney U
- **Why this test**: right-skewed continuous feature (skew 1.75 among active customers);
  t-test normality assumption does not hold.

- **Driver**: `total_spend` and `n_txn` (lifetime volume)
- **Test**: Mann-Whitney U
- **Why this test**: both are right-skewed (`total_spend` skew 1.03, `n_txn` skew 0.71);
  Mann-Whitney is safer than t-test here.

- **Driver**: `tenure_days`
- **Test**: t-test (after checking normality) or Mann-Whitney U if the assumption fails
- **Why this test**: `tenure_days` is roughly symmetric (skew −0.03) among all 1,500
  customers, so a t-test is plausible — but the direction of the association flips
  between all customers (shorter tenure → more churn, AUC 0.346) and active-only
  customers (longer tenure → more churn, AUC 0.547), so the analysis must separate
  the two populations and state which result it is reporting.

- **Driver**: `return_rate` per customer
- **Test**: Mann-Whitney U
- **Why this test**: zero-inflated (953 of 1,419 active customers have return_rate = 0,
  median 0, skew ~4.1); separation in Stage 0 was near-zero (AUC 0.518–0.537), so this
  may not be worth pursuing, but include it for completeness.

## Leakage / imbalance / non-stationarity / multi-source flags

- **Leakage**: `days_since_last_txn`, `txn_last_90d`, and `spend_last_90d` are all
  circular with the churn label. The label is defined as no purchase in the trailing
  90 days; any feature computed over that same window is not a predictor of churn —
  it is a re-expression of the label itself. Among active customers, `days_since_last_txn`
  achieves a single-feature ROC-AUC of 1.000 and a 90-day cutoff reproduces the churned
  label for 100% of them — that is a sign of leakage, not a useful signal. These three
  features must be excluded from any model-family reasoning and from the feature set
  passed to the build stage.

- **Imbalance**: overall churn rate is 13.47% (202 of 1,500); among the 1,419 active
  customers it is 8.53% (121 of 1,419). Always predicting "not churned" achieves 86.53%
  accuracy overall and 91.47% on active customers — accuracy is therefore not a usable
  evaluation metric. Use PR-AUC as the primary metric; report ROC-AUC alongside, with
  recall at a fixed precision or top-decile lift. Use stratified cross-validation and
  class weights.

- **Non-stationarity**: monthly transaction volume rises from 1 in 2024-02 to 1,231 in
  2026-07 (Spearman ρ = 0.998 with time), a +235% year-on-year increase. The trend is
  not strictly monotonic (month-on-month declines in 2024-11, 2025-11, 2026-02), and
  the customer mix shifts: the 2026 Q2 signup cohort churns at 37.4% across all customers
  but 0% among active ones. A random customer-level train/test split could overstate
  performance because early and late cohorts behave very differently. Prefer an out-of-time
  check; that requires backdated label snapshots, which this pass did not build.

- **Multi-source**: re-aggregating `transactions.db` to customer × month and comparing
  against `transactions_monthly_agg.parquet` month by month shows exact agreement for
  29 of 30 months. July 2026 disagrees: the parquet has 994 transaction-count units vs.
  1,231 in the row-level table (gap: 237 transactions, 19.3% of the month). The parquet
  appears to have been extracted through 2026-07-25 only. As a result, 10 customers whose
  first purchase fell in the last 6 days of July are absent from the parquet entirely,
  all labelled `churned = 0`. Counting zero-activity from the parquet would give 91
  instead of 81, incorrectly mixing 10 retained customers into an otherwise 100%-churned
  group. Use `transactions.db` as the source of truth; use the parquet only for months
  through 2026-06 where it agrees exactly.

## Model-family judgment

- **Candidate family**: gradient-boosted decision trees (LightGBM, XGBoost, or
  scikit-learn `HistGradientBoostingClassifier`)
- **Why, tied to this dataset's checked characteristics**: the dataset is small (1,419
  active customers, 121 positives) and tabular with mixed types (skewed continuous
  features, low-cardinality categoricals). Trees are scale-invariant and robust to the
  strong right skew in `amount` (skew 6.11), `total_spend`, and `avg_order_value`, so
  no log transforms are required. The non-leakage continuous drivers show moderate
  separation (purchase-rate AUC 0.735, lifetime-volume AUC ~0.60), and tenure shows a
  non-linear direction flip between populations — a tree captures both without
  hand-engineered interaction terms. Class weights (`scale_pos_weight`) handle the 8.53%
  active-customer churn rate without resampling.
- **Alternative considered**: L2-regularised logistic regression — **Why not the top
  pick**: reaching what trees get by default would require hand-built features (log
  transforms for skewed monetaries, binning or splines to capture threshold effects,
  explicit interaction terms for the tenure flip); keep it as the required baseline.
- **Drivers assumed usable**: `txn_per_30d_tenure`, `total_spend`, `n_txn`,
  `n_categories`, `tenure_days` (with population caveat), `acquisition_channel`,
  `region`, `dominant_category` (after fixing the tie-break rule).
- **Drivers excluded (leakage-tainted)**: `days_since_last_txn`, `txn_last_90d`,
  `spend_last_90d` — circular with the trailing-90-day label definition.
- **Drivers likely to drop (near-zero separation)**: `return_rate`, `avg_order_value`,
  channel-share features, `dominant_channel` (store-channel gap does not survive an
  alternative tie-break rule).
