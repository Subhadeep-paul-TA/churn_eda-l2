# Model-Family Recommendation: DRAFT (Stage 0 first pass, not verified)

> **This is a best-effort first pass, not a verified recommendation.** Claude generated it with the `churn-eda-profiling` skill (Stage 0). **No model has been trained, and no families have been compared.** The reasoning rests only on what the first-pass EDA in `notebooks/eda_stage0_first_pass.ipynb` showed, and that EDA is unreviewed itself (see `EDA_FINDINGS_DRAFT.md`). It also depends on an assumed as-of date of 2026-07-31. Expect the review step to challenge it.
>
> `skill.md` says this draft should meet the bar set in its "Domain Context" section. The repo's `skill.md` does not contain a section with that name, so this draft has not been checked against it.

---

## Candidate family

**Gradient-boosted decision trees** (LightGBM, XGBoost, or scikit-learn's `HistGradientBoostingClassifier`), predicting `churned` per customer. An **L2-regularised logistic regression** serves as the required baseline the trees must beat.

## Why, tied to what the first pass actually saw

1. **The data is small, tabular and mixed-type.** There are 1,500 customers, 1,419 with transactions. Each has around a dozen derived numeric features plus a few low-cardinality categoricals: `acquisition_channel` (4 levels), `region` (4) and dominant category (6). Tree ensembles are a strong default in this regime. [computed]
2. **The monetary features are heavily skewed, with long tails.** Transaction `amount` has skew 6.11, `avg_order_value` 2.87 and `total_spend` 1.03, and `return_rate` is zero-inflated. Trees are invariant to monotone transforms and robust to tails, so there is no need for log transforms or winsorising to get started. That also makes the unresolved outlier-rule question (783 vs. 86 flagged) matter less. [computed]
3. **The strongest signal is a sharp threshold.**
   - Among active customers, `days_since_last_txn` splits churners from retained customers cleanly at 90 days, with a single-feature AUC of 1.000.
   - Trailing-90-day transaction count and spend are just as clean.
   - A tree captures a step like this in one split. A linear model only approximates it unless the feature is binned.

   [computed]
4. **There are non-linear and interaction effects.**
   - Tenure's relationship with churn flips direction depending on whether zero-activity customers are included (AUC 0.346 across all customers vs. 0.547 among active).
   - Among active customers, churn by tenure bucket rises and then dips: 0.0% (≤90d) up to 11.2% (366–540d), then 9.0% (541–900d).
   - Trees pick this up without hand-built interaction terms.

   [computed numbers; the cause of the flip is not understood]
5. **The class imbalance is manageable.** Churn is 13.47% overall and 8.53% among active customers. Class weights (`class_weight` / `scale_pos_weight`) should be enough as a first step, with no resampling. [computed]

**Expected performance (first-pass expectation):**
- Recency and trailing-90-day activity already separate the classes perfectly among active customers in this snapshot. A 90-day recency cut-off alone reproduces the label for 100.00% of them. So a very high ROC-AUC on this snapshot should be easy to reach.
- The weaker features would mainly refine the ranking: purchase rate (separation 0.735), lifetime spend/frequency (about 0.60), acquisition channel, region, and dominant category.

## Alternative considered: L2-regularised logistic regression

**For it:**
- Coefficients are interpretable.
- Probabilities come out reasonably calibrated.
- There is less overfitting risk with only **202 positives (121 among active customers)**.
- It is easy to explain to stakeholders.

**Why it is not the top pick:**
- Reaching what trees get by default would take hand-built features: log transforms for the skewed spend features, binning or splines to capture the 90-day recency step, and explicit terms for the tenure flip.

**Keep it as the baseline.** If the trees don't clearly beat it in cross-validation, prefer logistic regression for its simplicity and interpretability.

**Other families considered and set aside (briefly):**
- **Survival / time-to-event models** (Cox, discrete-time hazard): the label provided is a single binary snapshot with no event times. These could be worth revisiting if churn is ever redefined as time-to-churn.
- **Neural networks and sequence models:** too little data (1,500 customers).

## Features this draft assumes are usable

| Group | Features | First-pass evidence |
|---|---|---|
| Recency | `days_since_last_txn` | separation 1.000: the top signal |
| Trailing-90-day activity | `txn_last_90d`, `spend_last_90d` | separation 1.000 |
| Purchase rate | `txn_per_30d_tenure` | 0.735 |
| Lifetime volume | `total_spend`, `n_txn`, `n_categories` | 0.608 / 0.604 / 0.592 |
| Tenure | `tenure_days` | 0.547 among active; direction flips with population |
| Categorical | `acquisition_channel`, `region`, `dominant_category` | descriptive gaps only, untested; `dominant_category` is tie-sensitive |
| Likely to drop | `return_rate`, `avg_order_value`, channel shares, `dominant_channel` | separation 0.518–0.537; the store-channel gap does not survive a different tie-break |

## Handling the 81 zero-activity customers

- These customers have no transaction features. All 81 are churned, which makes them 40.1% of churners.
- **Option A (leaning this way for simplicity):** handle them as a separate segment. The model is trained on the 1,419 active customers, and zero-activity customers are scored by rule, since every one of them is churned in this snapshot.
- **Option B:** keep them in the model with a `has_any_transaction` indicator and native missing-value handling. LightGBM and XGBoost both handle `NaN` natively.

## Evaluation plan

- **Primary metric:** PR-AUC (average precision). Report ROC-AUC alongside, plus recall at a fixed precision or top-decile lift. **Do not use accuracy.** Always predicting "not churned" already scores 86.53% overall and 91.47% on active customers.
- **Validation:** stratified 5-fold cross-validation, given the small positive class.
- **Out-of-time check:** transaction volume grows strongly over the period (Spearman 0.998; 367 → 1,231 transactions/month year on year), so an out-of-time check is worth having. Only one label snapshot exists, so a true out-of-time split would need backdated snapshots. This pass did not build them.
- **Calibration:** check it before using the scores as probabilities for targeting.

## Confidence and open questions

- **Overall confidence: low to medium.** No model was trained, and trees vs. logistic regression has not been compared on this data. With only 202 positives, the trees' advantage is not established.
- **The as-of date matters.** All recency and trailing-window features use the assumed as-of date of 2026-07-31. If the real one differs, they all have to be recomputed and this reasoning revisited.
- **Use `transactions.db` for features.** The parquet extract is missing the last 6 days of July 2026, so recent-window features built from it would be wrong.
- **The data issues could change this recommendation.** See `DATA_ISSUES_DRAFT.md`, especially non-stationarity and the multi-source gap.
