# eda_review.md — Churn EDA & Model-Family Recommendation

## Distribution / missingness / outlier corrections

- **Correction (amount distribution shape)**: Stage 0's draft (`EDA_FINDINGS_DRAFT.md` §5 & §10) eyeballed `transactions.amount` as "roughly log-normal" based solely on log10 skewness (-0.01) without running a formal goodness-of-fit test. We recomputed the distribution metrics directly from `transactions.db`: mean is $49.72, median is $33.82, Q1 is $18.36, Q3 is $61.39, IQR is $43.03, sample skewness is 6.11, and max is $1,684.21. A formal normality test on $\log_{10}(\text{amount})$ (Shapiro-Wilk test on sample: $W = 0.9992, p = 0.017$; D'Agostino-Pearson $p = 0.157$) shows that true log-normality does not hold cleanly due to discrete retail price clustering and an artificial spike of 52 transactions (0.44%) at exactly the $3.00 minimum price.

- **Correction (outlier rule choice and thresholds)**: Stage 0's draft left the outlier threshold undecided (`[choice of rule: low confidence]`), presenting raw 1.5×IQR (flagging 783 transactions or 6.67% above $125.93) vs. log-scale 1.5×IQR (flagging 86 transactions). In our check: the 75th percentile (Q3) of amount is $61.39, with an IQR of $43.03, which puts the upper 1.5×IQR fence at $125.93 ($61.39 + 1.5 \times 43.03$). Flagging 783 transactions (6.67%) on the raw scale arbitrarily cuts off the natural right tail of valid customer purchases (the top 10 transactions range from $562.86 to $1,684.21 across valid merchandise categories). On the log scale, the lower fence of $3.003 flags all 52 transactions sitting at the $3.00 floor as "low outliers". Neither rule should be used to drop or clip rows for downstream modeling; gradient-boosted trees are invariant to monotonic transformations, and for reporting, median ($33.82) and IQR ($43.03) should be used instead of mean and std.

- **Correction (tenure distribution and normality)**: Stage 0's draft noted `tenure_days` as "roughly symmetric (skew −0.03)" and suggested a standard t-test. Computing tenure from `customers.csv` as of 2026-08-01 yields: min 31 days, max 899 days, mean 468.6 days, median 469.0 days, and sample skewness -0.030. While skewness is close to zero, a D'Agostino-Pearson normality test yields $K^2 = 1104.96$ with $p = 1.15 \times 10^{-240}$. Tenure is essentially a uniform distribution across customer acquisition cohorts rather than a Gaussian bell curve, strongly violating the normality assumption required for Student's t-test. Non-parametric testing (Mann-Whitney U) must be used.

- **Correction (zero-activity counting across data sources)**: `DATA_ISSUES_DRAFT.md` §4 noted that `transactions_monthly_agg.parquet` was extracted through 2026-07-25. We verified this by re-aggregating `transactions.db` and comparing against the parquet extract: in `transactions.db`, exactly 81 customers have zero rows (5.40% of 1,500), all 81 are churners (`churned = 1`, making up 40.10% of all 202 churners). In `transactions_monthly_agg.parquet`, exactly 91 customers appear to have zero rows. The 10 customers present in the database but missing from the parquet (who transacted between July 26 and July 31) are all retained customers (`churned = 0`). Counting zero-activity from the parquet extract would misclassify those 10 active retained customers as zero-activity, distorting the zero-activity churn rate from 100.0% down to 89.01% (81 of 91). `transactions.db` must be used.

## Hypothesis tests to run

Stage 0 ran zero significance tests or p-values (§10 item 2). We recomputed each test statistic, degree of freedom, and p-value directly from `data/`:

- **Driver**: `acquisition_channel`
- **Test**: Chi-square test of independence
- **Why this test & findings**: 4-level unordered categorical predictor vs binary churn outcome across 1,500 customers. Recomputed from `customers.csv`: $\chi^2 = 5.8387, df = 3, p = 0.1197$. Churn rates by channel: paid_search 10.21% (44/431), referral 13.90% (41/295), social 14.55% (24/165), organic 15.27% (93/609). Because $p > 0.05$, the observed descriptive differences are not statistically significant.

- **Driver**: `region`
- **Test**: Chi-square test of independence
- **Why this test & findings**: 4-level categorical predictor vs binary churn outcome across 1,500 customers. Recomputed from `customers.csv`: $\chi^2 = 3.7571, df = 3, p = 0.2889$. Churn rates by region: north 12.34% (47/381), west 12.37% (47/380), south 12.71% (45/354), east 16.36% (63/385). Not statistically significant at $\alpha = 0.05$.

- **Driver**: `txn_per_30d_tenure` (purchase rate)
- **Test**: Mann-Whitney U test
- **Why this test & findings**: Continuous, right-skewed feature (skew 1.75 among active customers) comparing churned vs retained active customers. Recomputed: $U = 41677.0, p = 1.25 \times 10^{-17}$. Median purchase rate for churners is 0.335 transactions per 30 days vs 0.512 for retained customers. Statistically significant; retained customers purchase at a substantially higher frequency throughout their tenure.

- **Driver**: `total_spend` and `n_txn` (lifetime customer volume)
- **Test**: Mann-Whitney U test
- **Why this test & findings**: Continuous right-skewed monetary spend (skew 1.03) and discrete count (skew 0.71). Recomputed: for `total_spend`, $U = 61626.5, p = 8.83 \times 10^{-5}$ (churn median $282.39 vs retained median $364.38); for `n_txn`, $U = 62236.5, p = 1.53 \times 10^{-4}$ (churn median 6.0 vs retained median 8.0). Both are statistically significant drivers among active customers.

- **Driver**: `tenure_days`
- **Test**: Mann-Whitney U test
- **Why this test & findings**: Bounded, non-normal uniform distribution ($p < 10^{-200}$). The relationship flips depending on population: across all 1,500 customers, churners have significantly shorter tenure ($U = 90686.0, p = 1.71 \times 10^{-12}$; churn mean 351.7 days vs retained 486.8 days) because all 81 zero-activity customers signed up recently. Among the 1,419 active customers alone, the relationship reverses ($U = 85934.5, p = 0.0859$; churn mean 528.1 days vs retained 486.8 days), which is not statistically significant at $\alpha = 0.05$.

- **Driver**: `return_rate`
- **Test**: Mann-Whitney U test
- **Why this test & findings**: Zero-inflated bounded ratio (953 of 1,419 active customers have return_rate = 0.0, skew 4.08). Recomputed: $U = 75246.5, p = 0.3618$. Median return rate is 0.000 for both churned and retained customers. The difference is not statistically significant; return rate should not be prioritized as a churn predictor.

## Leakage / imbalance / non-stationarity / multi-source flags

- **Leakage**: `days_since_last_txn`, `txn_last_90d`, and `spend_last_90d`. The churn label is defined in the assignment brief as having no transactions in the trailing 90 days before the as-of date (2026-08-01). Any feature calculated over that trailing 90-day window is definitionally circular with the ground truth label. In Stage 0, `days_since_last_txn` achieved a single-feature ROC-AUC of 1.000 (all 121 active churners have $\ge 91$ days recency; all 1,298 active retained customers have $\le 90$ days). This is tautological leakage that inflates validation metrics artificially. These three features must be excluded from all model training and evaluation.

- **Imbalance**: Overall churn rate is 13.47% (202 of 1,500); active customer churn rate is 8.53% (121 of 1,419). Naive accuracy (predicting all customers "not churned") achieves 86.53% overall and 91.47% on active customers. Accuracy is completely uninformative. Performance must be evaluated using PR-AUC (average precision), precision-recall curves, and top-decile lift, supported by stratified cross-validation and class weighting (`scale_pos_weight`).

- **Non-stationarity**: Monthly transaction volume expands from 1 transaction in 2024-02 to 1,231 in 2026-07 (Spearman rank correlation with time $\rho = 0.9978, p < 10^{-25}$). Year-on-year volume rose +235.4% (from 367 in 2025-07 to 1,231 in 2026-07). The upward drift is driven by customer base accumulation (signups 40–74 per month). Furthermore, churn behavior differs by cohort (e.g. 2026 Q2 signups churn at 37.4% overall vs 0.0% among active customers). A standard random train/test split would cross-contaminate cohorts; an out-of-time validation check is required.

- **Multi-source**: Re-aggregating `transactions.db` to customer × month against `transactions_monthly_agg.parquet` confirms exact agreement for 29 of 30 months. July 2026 diverges: `transactions.db` contains 1,231 transactions, $62,084.62 total amount, and 68 returns; `transactions_monthly_agg.parquet` contains 994 transactions, $50,116.67, and 51 returns. The parquet extract is missing 237 transactions (19.25%), $11,967.95 (19.28%), and 17 returns because it was extracted on 2026-07-25. Ten customers whose first transaction occurred between July 26 and July 31 are entirely absent from the parquet file. Using the parquet would falsely count 91 zero-activity customers (diluting churn rate to 89.01%) instead of 81 (100% churn). `transactions.db` must be the sole source of truth.

## Model-family judgment

- **Candidate family**: Gradient-boosted decision trees (e.g., LightGBM, XGBoost, or scikit-learn's `HistGradientBoostingClassifier`).
- **Why, tied to this dataset's checked characteristics**: Stage 0's draft cited the sharp 90-day recency separation to argue for tree models; that reasoning is invalid because that feature is circular leakage. However, tree ensembles remain the defensible top choice for legitimate data characteristics: the dataset is small tabular mixed-type data (1,419 active customers, 121 positives; 81 zero-activity rule-handled). Key monetary and frequency features are heavily right-skewed (`amount` skew 6.11, `total_spend` skew 1.03), and tree partitioning is invariant to monotonic transformations, eliminating the need for arbitrary log-transforms or outlier clipping. Trees naturally capture non-linear relationships (such as tenure's non-monotonic relationship with churn among active customers) without manual interaction engineering, and natively support class weighting (`scale_pos_weight`) for the 8.53% active-customer churn rate.
- **Alternative considered**: L2-regularised logistic regression. **Why not the top pick**: Reaching comparable representation would require extensive manual feature engineering (log transforms for skewed monetaries, non-linear splines or interaction terms for tenure/cohort effects); it is retained as the required baseline that tree ensembles must outperform.
- **Drivers assumed usable**: `txn_per_30d_tenure` (purchase rate), `total_spend`, `n_txn`, `n_categories`, `acquisition_channel`, `region`, `dominant_category` (with deterministic tie-breaking).
- **Drivers excluded (leakage-tainted)**: `days_since_last_txn`, `txn_last_90d`, `spend_last_90d`.
- **Drivers dropped (no signal / non-significant)**: `return_rate` ($p = 0.362$, AUC 0.52), `avg_order_value` (AUC 0.52), `dominant_channel` (tie-sensitive, non-significant).
