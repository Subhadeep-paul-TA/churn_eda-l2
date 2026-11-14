# Data Issues: DRAFT (Stage 0 first pass, not verified)

> **This is a best-effort first pass, not a verified issues log.** Claude generated it with the `churn-eda-profiling` skill (Stage 0), working directly from the raw files in `data/`. These are **candidate** flags from one unreviewed pass. Some are backed by a computed number. Some rest on an inference or an assumption, and each flag says which. It is not a complete audit, and the review step should expect to add, correct or drop items.
>
> Tags: **[computed]** means from code in `notebooks/eda_stage0_first_pass.ipynb`. **[eyeballed]** means descriptive and untested. **[assumption]** means not stated in the data.
>
> `skill.md` says this draft should meet the bar set in its "Domain Context" section. The repo's `skill.md` does not contain a section with that name, so this draft has not been checked against it.

---

## 1. Class imbalance [computed; confidence high on the numbers]

| Population | Churned | Rate | Accuracy of "always not churned" |
|---|---|---|---|
| All customers | 202 of 1,500 | **13.47%** | 86.53% |
| Active customers only | 121 of 1,419 | 8.53% | 91.47% |
| Zero-activity customers | 81 of 81 | 100% | n/a |

**What it implies:**
- Accuracy is not a usable headline metric. Use PR-AUC, recall at a fixed precision, or top-decile lift, with ROC-AUC as a secondary check.
- Use stratified cross-validation and class weights.
- If zero-activity customers are split off (see §5), the modelled population is even more imbalanced: 8.53%, or 121 positives.

## 2. Non-stationarity [computed trend; the decomposition is eyeballed]

- Monthly transactions rise from **1 in 2024-02 to 1,231 in 2026-07**. The Spearman rank correlation with time is **0.998**.
- **The rise is not monotonic.** There are 3 month-over-month declines: 2024-11, 2025-11 and 2026-02.
- Year on year, 2025-07 → 2026-07 went from 367 to 1,231 transactions (+235%).
- **[eyeballed]** The growth looks like mostly an accumulating customer base:
  - New signups are roughly flat at 40–74 per full month (median 50).
  - Transactions per active customer drift up only modestly (1.34–1.56 over the last 12 months).
  - Average ticket (\$46.64–\$55.15) and return rate (3.2%–6.3%) look flat.
- **[computed]** The customer mix shifts over time. Recent signup cohorts behave very differently: 2026Q2 churns at 37.4% across all customers but 0.0% among active ones.

**What it implies:**
- A model fitted on this one snapshot may not transfer to a later as-of date.
- A random customer split could overstate performance.
- Prefer an out-of-time check. That needs backdated label snapshots, which this pass did not build.

**Confidence:** high that volume and mix are non-stationary; medium on why.

## 3. Candidate leakage: checks run in this pass

| Check | Result | Note |
|---|---|---|
| Transactions dated after the as-of date | 0 | **True by construction.** `AS_OF` was *set* to the last transaction date, so this is not evidence of anything. |
| Transactions dated before the customer's `signup_date` | 0 | [computed] |
| Transactions whose `customer_id` is not in `customers.csv` | 0 | [computed] |
| Exact duplicate transaction rows | 0 | [computed] |
| Parquet rows for months after `AS_OF` | 0 | [computed] |
| Customers with `signup_date` after `AS_OF` | 0 | [computed] |

- **[assumption] As-of date.** None of the files records when `churned` was computed. This pass used **2026-07-31**, the last transaction date. If the true as-of date is earlier, then two things change:
  - Transactions after it must be excluded from every feature.
  - Recency, tenure and the trailing-90-day features all have to be recomputed.

  **Confidence: low.** This needs confirming before any feature work.
- **This is not a complete leakage audit.** Only the checks in the table were run.

## 4. Multi-source disagreement: parquet extract vs. row-level table [computed; cutoff date inferred]

**Month level**
- Re-aggregating `transactions.db` by month matches `transactions_monthly_agg.parquet` **exactly for 29 of 30 months**.
- **2026-07 disagrees.** The row-level table has 1,231 transactions and \$62,084.62; the parquet has 994 and \$50,116.67.
- So **237 transactions (19.3%), \$11,967.95 (19.3% of the month's amount) and 17 returns are missing from the parquet.**

**Customer × month**
- The row-level table has 8,188 customer-months; the parquet has 8,086.
- 102 customer-months are row-level only and 110 are in both but with different values. None are parquet only.
- **Every disagreement is in 2026-07.**

**Probable cause** [inferred from one probe]
- Keeping only row-level July transactions timestamped before **2026-07-26** reproduces the parquet's July rows exactly for every customer. No other daily cutoff does.
- So the parquet looks like it was **extracted with data through 2026-07-25**, dropping the last 6 days.
- Exactly 237 row-level transactions are dated 2026-07-26 or later, which is the same number as the gap.

**Consequences:**
- **10 customers** whose first-ever purchase was between 2026-07-26 and 2026-07-30 are **absent from the parquet entirely**. All 10 are `churned = 0`.
- Counting zero-activity customers from the parquet would give **91 instead of 81**, and would mix 10 retained customers into an otherwise 100%-churned group.
- Any recency or trailing-window feature built from the parquet would be wrong for the last 6 days of the window. July 2026 volume would also look flat or down in a trend chart.
- **Recommendation:**
  - Treat `transactions.db` as the source of truth.
  - Use the parquet, if at all, only for months up to 2026-06, where it agrees exactly.

## 5. Population and label observations

- **Zero-activity customers** [computed]:
  - 81 customers (5.4%) have no transactions, and **all 81 are labelled churned**. That is 40.1% of all churners.
  - 80 of 81 signed up in 2026 (2025-06-20 → 2026-07-01).
  - Every transaction-derived feature is undefined for them.
  - **Open question:** should they be modelled together with customers who transacted and stopped, or handled as their own segment? This needs a decision before modelling.
- **The tenure / cohort direction flips** [computed; interpretation low confidence]:
  - Across all customers, short tenure means more churn: 46.5% for ≤90 days, AUC 0.346.
  - Among active customers, the same bucket churns at 0.0%, and churn rises with tenure (AUC 0.547).
  - Any tenure-based conclusion is confounded with the zero-activity group until the flip is understood.
- **The customer table stops at 2026-07-01 signups** [computed; cause unknown]:
  - No signup is later than 2026-07-01, so the minimum tenure at `AS_OF` is 30 days.
  - There are only 3 signups in July 2026, against 49 in June.
  - This could be an eligibility rule ("customers at least 30 days old") or an extract cutoff. Nothing documents it.

## 6. Value-level issues

- **A \$3.00 floor on `amount`** [computed; cause guessed]:
  - 52 transactions (0.44%) sit at exactly \$3.00, against only 25 in the next 50 cents.
  - They are exactly the 52 "low outliers" on a log scale.
  - This looks like a floor or clip rather than genuine purchases.
- **Long right tail on `amount`** [computed; rule choice low confidence]:
  - Skew is 6.11 and the maximum is \$1,684.21.
  - 1.5×IQR on the raw scale flags 783 transactions (6.7%) above \$125.93. On the log scale the same rule flags 86.
  - Which rule is appropriate, and whether the largest amounts are genuine, has not been checked.
- **`dominant_category` / `dominant_channel` depend on the tie-break rule** [computed]:
  - The top value is tied for 36.1% of active customers on category and 18.5% on channel.
  - Changing the tie-break moves the store-channel churn rate from 11.1% to 9.4%, and apparel's group size from 361 to 154.
  - Any driver built on these features needs an explicit, documented tie-break rule.

## 7. Not checked in this pass

- No hypothesis tests or p-values. Every candidate driver is descriptive only.
- The as-of date has not been confirmed against any documentation.
- No complete leakage audit (§3 lists everything that was run).
- No formal trend decomposition and no backdated snapshots.
- No verification that the largest transaction amounts are genuine, and no explanation of the \$3.00 floor.
