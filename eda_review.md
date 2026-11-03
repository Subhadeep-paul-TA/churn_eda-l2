# eda_review.md — Churn EDA & Model-Family Recommendation

<<LEARNER: fill in the SKELETON section below yourself, against skill.md's Domain Context
section and Stage 0's generated first-pass notebook/draft findings — correct that draft,
don't restate it. Do this before opening Claude Code for the build stage. See the EXAMPLE
section below (and Helper Guide.docx) for what a filled-in answer looks like — the example
uses a return-rate-by-channel hypothesis, which is NOT necessarily one of this dataset's real
findings once you check it, so it can't be copied in as your own answer. Delete the EXAMPLE
section and every bracketed prompt in the SKELETON before you submit.>>

---

## EXAMPLE — reference only, delete before submitting

**Distribution / missingness / outlier corrections**
- Correction: Stage 0's draft called `amount` "roughly normal" — checked mean ($49.72) vs.
  median ($33.82); the gap plus a max of $1,684 against a 75th percentile of $61 says
  right-skewed with real high-value outliers, not normal. Flagging any monetary summary
  stat downstream should use median/IQR, not mean/std.
- Correction: Stage 0's draft counted the 81 zero-activity customers as "5% missing
  transaction data" — they are not missing, they legitimately have zero rows in
  `transactions.db`; relabeled as a zero-activity population, not a data-quality gap.

**Hypothesis tests to run**
- Driver: acquisition_channel — Test: chi-square (categorical vs. binary churn) — Why:
  categorical predictor, categorical-ish outcome, no ordering assumption needed.
- Driver: return_rate — Test: Mann-Whitney U — Why: return_rate is bounded and zero-inflated
  for most customers, not normal, so a t-test's normality assumption doesn't hold.

**Leakage / imbalance / non-stationarity / multi-source flags**
- Leakage: Stage 0's draft reported "days_since_last_txn is the single best predictor" as
  good news — it is not: the churn label is defined as no purchase in the trailing 90 days,
  so this feature (and trailing-90-day spend) is circular with the label, not predictive of
  it. Excluding both from any model-family reasoning.
- Imbalance: churn rate needs to be stated as a number and checked before assuming accuracy
  is a usable metric.
- Non-stationarity: monthly transaction volume needs to be checked for a trend before
  assuming a random train/test split is safe.
- Multi-source: transactions.db reaggregated to customer x month needs to be compared
  against transactions_monthly_agg.parquet month by month, not assumed to agree.

**Model-family judgment**
- Candidate family: <<state one, with reasoning tied to the actual checked characteristics
  above>> — Alternative considered: <<one>> — Why not the top pick: <<one phrase>>

---

## SKELETON — fill this in

## Distribution / missingness / outlier corrections

<<At least one real correction to Stage 0's draft, per skill.md's Domain Context: a
distribution/skew claim that didn't hold up numerically, an outlier rule that was too
loose/strict, or a missingness claim that conflated zero-activity with actually missing.>>
- **Correction**: <<what Stage 0's draft said>> vs. <<what you found checking it yourself,
  with the actual number>>

## Hypothesis tests to run

<<One block per candidate churn-driver, per skill.md's Domain Context: name, the test that
matches the variable's actual shape, and why. Add/remove freely — this is not a fixed list.>>
- **Driver**: <<name>>
- **Test**: <<chi-square / Mann-Whitney U / t-test / other, matched to the variable's shape>>
- **Why this test**: <<one phrase>>

## Leakage / imbalance / non-stationarity / multi-source flags

<<At minimum, per skill.md's Domain Context: (1) which candidate driver(s), if any, are
leakage-tainted by the trailing-90-day label definition, and why; (2) the churn-rate number
and which metric(s) it makes misleading; (3) whether the monthly volume trend is checked and
what it implies for train/test splitting; (4) whether the row-level table and the monthly
aggregate are actually compared month by month, and what that comparison should look for.>>
- **Leakage**: <<name the tainted variable(s), or state none apply and why>>
- **Imbalance**: <<what to check, and which metric(s) it would rule in/out>>
- **Non-stationarity**: <<what to check, and the modelling consequence if present>>
- **Multi-source**: <<what comparison to run, and what a real disagreement would look like>>

## Model-family judgment

<<Per skill.md's Domain Context: a candidate family tied to this dataset's actual checked
characteristics (not a generic pick), an alternative you considered, and why it wasn't the
top choice. State explicitly which candidate drivers you are and are not assuming are usable,
given the leakage flags above.>>
- **Candidate family**: <<name>>
- **Why, tied to this dataset's checked characteristics**: <<one or two sentences>>
- **Alternative considered**: <<name>> — **Why not the top pick**: <<one phrase>>
- **Drivers assumed usable / excluded**: <<list>>
