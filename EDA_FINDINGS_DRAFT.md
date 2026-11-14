# EDA Findings: DRAFT (Stage 0 first pass, not verified)

> **This is a best-effort first pass, not a verified analysis.** Claude generated it with the `churn-eda-profiling` skill (Stage 0), working directly from the three raw files in `data/` with no `eda_review.md` to lean on. Nobody has reviewed it or re-derived it independently. Some claims are computed, some are eyeballed from descriptive splits, and one key input (the as-of date) is assumed. Expect the review step to find things here that need correcting.
>
> Every claim carries one of these tags:
> - **[computed]**: the number comes from code in `notebooks/eda_stage0_first_pass.ipynb`. The interpretation next to it can still be wrong.
> - **[eyeballed]**: read off a chart or a descriptive split. No statistical test was run.
> - **[assumption]**: the data does not state it, so I had to assume it.
>
> `skill.md` says these drafts should meet the bar set in its "Domain Context" section. The repo's `skill.md` does not contain a section with that name, so this draft has not been checked against it.

All numbers come from `notebooks/eda_stage0_first_pass.ipynb`, which runs top to bottom. `§n` refers to its section numbers. Companion drafts: `MODEL_RECOMMENDATION_DRAFT.md` and `DATA_ISSUES_DRAFT.md`.

---

## 1. The three sources at a glance (§1–2) [computed]

| Source | Rows | Grain | Columns | Date range |
|---|---|---|---|---|
| `customers.csv` | 1,500 | one row per customer (`customer_id` unique) | `customer_id`, `signup_date`, `acquisition_channel` (4 levels), `region` (4 levels), `churned` (0/1) | signups 2024-02-14 → 2026-07-01 |
| `transactions.db` (table `transactions`) | 11,742 | one row per transaction | `customer_id`, `txn_timestamp`, `category` (6), `channel` (3), `amount`, `is_returned` (0/1) | 2024-02-29 → 2026-07-31 |
| `transactions_monthly_agg.parquet` | 8,086 | customer × month (`(customer_id, txn_month)` unique) | `customer_id`, `txn_month`, `txn_count`, `total_amount`, `return_count` | 2024-02 → 2026-07 (30 months) |

- `txn_timestamp` is stored as **TEXT** in SQLite (ISO-8601 with nanosecond precision) and parses cleanly.
- `signup_date` is a plain `YYYY-MM-DD` string.
- `txn_month` in the parquet is a real timestamp and is always the first of the month.

## 2. Missingness (§3) [computed]

- **No nulls in any column of any source**, and no blank or whitespace-only strings in the text columns.
- There is nothing to impute. The absence that matters is structural: customers who have no transaction rows at all (next section). That is a different thing from a missing value and should not be counted as one.

## 3. The zero-activity customer population (§4) [computed]

- **81 of 1,500 customers (5.4%) have zero rows in `transactions.db`.** This was counted directly. The other 1,419 have at least one transaction.
- There are no orphan transactions: every `customer_id` in `transactions.db` exists in `customers.csv`.
- **All 81 are labelled `churned = 1`**, so they make up **81 of the 202 churners (40.1%)**.
- They are almost all recent signups: 80 of 81 signed up in 2026, and their signup dates run 2025-06-20 → 2026-07-01.
- They are spread across every channel and region. Their share is about 4–7% in each.
- Every transaction-derived feature (recency, spend, return rate, basket mix) is **undefined** for them. Counts and sums are genuinely 0, but ratios and recency do not exist. Dropping them would silently remove 40% of the positive class.

## 4. As-of date (§5) [assumption]

- None of the three files records the as-of date at which `churned` was computed. **I used `AS_OF = 2026-07-31`, the last transaction date.**
- Tenure, recency and the trailing-90-day features all depend on this. **Low confidence; needs confirming.**
- **[computed]** No `signup_date` is later than 2026-07-01, so every customer has at least 30 days of tenure at this `AS_OF`. There are 3 signups in July 2026 against 49 in June. That looks like either an eligibility rule or an extract cutoff on the customer table. Nothing documents which.

## 5. Distribution shape and outliers (§6)

Rules used:
- **Skew:** sample skewness, where |skew| ≤ 0.5 counts as "roughly symmetric".
- **Outliers:** Tukey 1.5 × IQR fences.

**`transactions.amount`** [computed]
- Strongly **right-skewed**: mean \$49.72 vs. median \$33.82, skew 6.11, p99 \$255.66, max \$1,684.21.
- On a log scale it is close to symmetric (log10 skew −0.01). **[eyeballed]** That suggests a roughly log-normal shape, but I have not done a formal fit.

**Outliers in `amount` depend heavily on the rule** [computed; choice of rule: low confidence]
- 1.5×IQR on the raw scale flags **783 transactions (6.7%)** above \$125.93. 3×IQR flags 273. This mostly looks like the natural long tail rather than errors.
- 1.5×IQR on the log scale flags **86** (34 high, 52 low).
- I have **not** decided which rule is appropriate, and I have **not** checked whether the largest amounts are genuine. The top ten run \$562.86–\$1,684.21 across all categories and channels.

**A pile-up at the minimum** [computed; cause guessed]
- **52 transactions (0.44%) sit at exactly \$3.00**, against only 25 in the next 50 cents.
- Those 52 are exactly the log-scale "low outliers".
- It looks like a floor or clip on `amount` rather than genuine small purchases. Nothing documents it.

**Parquet columns** [computed]
- All three are right-skewed.
- `txn_count` runs 1–6 (median 1). `total_amount` runs \$3.00–\$1,753.23. `return_count` runs 0–3 and is mostly 0.

**Returns** [computed]
- 591 of 11,742 transactions are returned (5.03%).

**Customer-level features** (§5–6) [computed]
- Built per customer as of the assumed `AS_OF`. Tenure covers all 1,500 customers; the rest cover the 1,419 active ones.
- Most spend and frequency features are right-skewed: `total_spend` skew 1.03, `avg_order_value` 2.87, `n_txn` 0.71, `txn_per_30d_tenure` 1.75.
- `return_rate` is **zero-inflated**: median 0, skew 4.08. Most customers never return anything.
- `tenure_days` is roughly symmetric (skew −0.03, range 30–898 days).
- `n_categories` leans slightly left (skew −0.51). Most customers buy across 4–6 categories.
- For any downstream summary of monetary features, use median/IQR rather than mean/std.

## 6. Category / channel / region breakdowns (§7) [computed]

- **Category:** transactions are spread almost evenly across the six categories, 1,911–2,008 each.
- **Channel:** web 45.0%, mobile_app 35.3%, store 19.7%.
- **Ticket size barely moves.** Median amount is \$32.96–\$34.73 by category and \$33.56–\$34.08 by channel.
- **Return rate is about 5% everywhere:** 4.70%–5.12% by channel and 4.49%–5.66% by category.
- The channel mix within every category is nearly identical: about 34–37% mobile_app, 18–21% store, 43–47% web.
- **Customers by region** are close to balanced, 354–385 each.
- **Customers by acquisition channel:** organic 40.6%, paid_search 28.7%, referral 19.7%, social 11.0%.

## 7. Churn rate and candidate drivers (§8–9)

### 7.1 Overall [computed]

| Population | Churned | Rate |
|---|---|---|
| All customers | 202 of 1,500 | **13.47%** |
| Active customers (≥1 transaction) | 121 of 1,419 | 8.53% |
| Zero-activity customers | 81 of 81 | 100% |

Always predicting "not churned" would score 86.53% accuracy, or 91.47% on active customers alone.

### 7.2 Headline finding: recency is the standout predictor [computed]

- **Among active customers, `days_since_last_txn` separates churners from retained customers perfectly in this snapshot**, with a single-feature ROC-AUC of **1.000**.
- Every churner is at 91 days or more (median 113). Every retained customer is at 90 days or fewer (median 23).
- **A 90-day recency cut-off reproduces the `churned` label for 100.00% of the 1,419 active customers.**
- The **trailing-90-day activity** features are just as clean. Every active churner has `txn_last_90d = 0` and `spend_last_90d = 0`, while retained customers have a median of \$103.29 in that window. Separation is 1.000 for both.
- This is by far the strongest signal in the first pass. Nothing else comes close.

### 7.3 Other numeric candidates (active customers) [computed separation; no tests run]

Separation is max(AUC, 1 − AUC) of the raw feature, a descriptive measure only. 0.5 means none and 1.0 means perfect.

| Feature | Median: churned vs. retained | Separation | Shape |
|---|---|---|---|
| `txn_per_30d_tenure` (purchase rate) | 0.335 vs. 0.513 | 0.735 | right-skewed |
| `total_spend` | \$282.39 vs. \$364.38 | 0.608 | right-skewed |
| `n_txn` | 6 vs. 8 | 0.604 | right-skewed count |
| `n_categories` | 4 vs. 4 | 0.592 | discrete 1–6 |
| `share_store` | 0.111 vs. 0.175 | 0.555 | bounded 0–1 |
| `tenure_days` | 507 vs. 486.5 | 0.547 | roughly symmetric |
| `avg_order_value`, `return_rate`, `n_returns`, `share_web`, `share_mobile_app` | close to equal | 0.518–0.537 | n/a |

- After recency, **purchase rate** is the most promising, and churners buy less often.
- Lifetime volume (`n_txn`, `total_spend`) is weaker.
- **`return_rate` and `avg_order_value` show essentially no separation.** Neither returns nor ticket size looks like a churn driver from this pass.

### 7.4 Categorical candidates [eyeballed: descriptive rates only, no test run]

| Candidate | All customers | Active only | Note |
|---|---|---|---|
| `acquisition_channel` | paid_search lowest (10.2%); organic 15.3%, social 14.5%, referral 13.9% | paid_search 6.1%; social 10.8%, organic 10.1%, referral 7.6% | 4 levels, 165–609 customers each |
| `region` | east highest (16.4%) vs. 12.3%–12.7% | east 11.3% vs. 7.5%–7.7% | 4 levels, 354–385 customers each |
| `dominant_category` (active only) | n/a | **grocery 3.3% (7 of 212)** vs. 7.9%–12.7%; electronics highest | 6 levels, **tie-sensitive (see below)** |
| `dominant_channel` (active only) | n/a | store 11.1% (16 of 144) vs. 8.2%–8.3% | **gap does not survive a different tie-break** |

- **Caveat on `dominant_*` features (low confidence).** The top value is tied for 36.1% of active customers on category and 18.5% on channel.
  - The main tables give ties to the alphabetically first value. Giving them to the alphabetically last value instead keeps **grocery lowest (3.3% → 3.1%)** and **electronics highest (12.7% → 12.4%)**, though group sizes swing a lot (apparel goes from 361 to 154 customers).
  - The **store-channel gap disappears** under the alternative rule: 11.1% → 9.4%, against 8.1%–9.2% for the other channels.
- Gaps of a few percentage points between groups of a few hundred customers can easily be noise. **None of these has been tested.**

### 7.5 Tenure and signup cohort: the direction flips (§8–9) [computed numbers; interpretation low confidence]

- **Across all customers, newer customers churn more:**
  - The 2026Q2 signup cohort churns at 37.4%.
  - The ≤90-day tenure bucket churns at 46.5%.
  - Tenure AUC is 0.346, so churners have shorter tenure.
- **Among active customers, the same groups churn at 0.0%**, and churn *rises* with tenure: 0.0% (≤90d), 4.3% (91–180d), 8.2% (181–365d), 11.2% (366–540d), then 9.0% (541–900d). Tenure AUC here is 0.547.
- The all-customer pattern is driven by the zero-activity customers, who are concentrated in recent cohorts. I have **not** worked out why the active-only direction goes the other way. Treat tenure as confounded with the zero-activity group until someone looks at it properly.

### 7.6 Candidate drivers worth formally testing (suggested, not run)

- **Categorical:** `acquisition_channel`, `region`, `dominant_category` (only after fixing the tie-break rule).
- **Continuous:** `txn_per_30d_tenure` (right-skewed), `total_spend` and `n_txn` (right-skewed), `tenure_days` (roughly symmetric, but the direction depends on population).
- **Probably not worth pursuing, on this evidence:** `return_rate` (zero-inflated, no separation), `avg_order_value`, the channel shares.
- Recency and trailing-90-day activity don't need a test to show they separate. Section 7.2 already shows they do, perfectly.

## 8. Monthly transaction-volume trend (§10) [computed; decomposition eyeballed]

- **Strong upward trend.** Volume goes from 1 transaction in 2024-02 to **1,231 in 2026-07**. The Spearman rank correlation with time is **0.998**.
- **It is not strictly monotonic.** There are 3 month-over-month declines: 2024-11, 2025-11 and 2026-02.
- Year on year, 2025-07 → 2026-07 went from 367 to 1,231 transactions (+235%).
- **[eyeballed]** The growth looks like mostly **customer-base growth** rather than customers buying more:
  - New signups are roughly flat at 40–74 per full month (median 50), so the base keeps accumulating.
  - Transactions per active customer only drift upward (1.34–1.56 over the last 12 months).
  - Average ticket (\$46.64–\$55.15) and return rate (3.2%–6.3%) look flat.
  - I have not formally decomposed this.
- Either way, volume and customer mix are **not stationary over the period**. See `DATA_ISSUES_DRAFT.md`.

## 9. Parquet extract vs. row-level table (§11) [computed; cutoff date inferred]

- Month-level totals agree **exactly for 29 of 30 months**.
- **2026-07 is short in the parquet by 237 transactions (19.3%), \$11,967.95 and 17 returns.**
- At customer × month grain, 102 customer-months are missing and 110 differ, all in 2026-07.
- Cutting the row-level data at **2026-07-26** reproduces the parquet exactly. So the extract looks like it only covers data **through 2026-07-25**.
- The consequence is that 10 customers are absent from the parquet entirely. Counting zero-activity from the parquet would give **91 instead of 81**.
- Details are in `DATA_ISSUES_DRAFT.md`. **Use `transactions.db` as the source of truth.**

## 10. What this draft did not check / lowest-confidence claims

1. **The as-of date (2026-07-31) is assumed**, not confirmed. Every time-relative number above depends on it.
2. **No hypothesis tests and no p-values were run.** Every "driver" in §7.3–7.4 is a descriptive gap or a separation score only.
3. The outlier rule for `amount` is undecided (783 vs. 86 flagged). The \$3.00 floor and the largest amounts have not been explained.
4. The `dominant_*` features depend on the tie-break rule. The store-channel gap is likely noise.
5. The tenure direction flip is not understood.
6. The trend decomposition (customer-base growth vs. intensity) is eyeballed, not modelled.
7. The parquet cutoff date (2026-07-25) is inferred from a single probe.
8. The "roughly log-normal" description of `amount` is eyeballed.
9. This is not a full leakage audit. Only the checks listed in `DATA_ISSUES_DRAFT.md` §3 were run.
