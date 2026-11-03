# Churn EDA & Model-Family Recommendation

## Overview

This skill runs a problem-type-appropriate exploratory data analysis on the e-commerce
customer churn dataset in `data/` — the same three heterogeneous sources used in the
companion feature-pipeline assignment (a CSV, a SQLite database, and a parquet extract), this
time to characterize the data rather than to build features from it. It profiles
distributions, missingness, and outliers; tests candidate churn-driver hypotheses with an
appropriate statistical test per variable; checks for time-drift and a multi-source
disagreement between the row-level table and the monthly aggregate; flags leakage risk and
class imbalance; and produces a defensible model-family recommendation. It implements an
already-confirmed `eda_review.md` — it does not write the review itself.

## Files in This Skill

- `skill.md` — the full build spec Claude follows: purpose, required inputs, the repo
  scaffold, the step-by-step workflow (data load, profiling, hypothesis testing, time/leakage
  checks, findings/recommendation/issues docs, tests, self-review), guardrails, and the
  validation checklist.
- `README.md` — this file.
- No `assets/` folder — this skill needs no templates, sample prompts, or reference diagrams
  beyond what `skill.md` already specifies.

## How Learners Should Use This

1. Invoke this skill's Stage 0 first, before `eda_review.md` exists at all: ask Claude to
   generate a first-pass EDA notebook and draft findings (`EDA_FINDINGS_DRAFT.md`,
   `MODEL_RECOMMENDATION_DRAFT.md`, `DATA_ISSUES_DRAFT.md`) directly from the raw sources.
   Treat the output as best-effort, not authoritative.
2. Read that generated output in full, on your own, and spot-check at least one distribution,
   outlier, or hypothesis claim in it against the actual data — with no help from Claude.
3. Correct `eda_review.md` from Stage 0's drafts against `skill.md`'s Domain Context section
   (the standard for what a real distribution/outlier claim, hypothesis test, leakage flag,
   imbalance flag, non-stationarity flag, multi-source finding, and model-family
   recommendation need to look like) — a real review, not a rubber stamp, recording at least
   one thing you found wrong or under-justified in Stage 0's output — see
   `Helper Guide.docx`.
4. Reconcile your corrected review with Claude in a separate conversation, without invoking
   this skill's build stage.
5. Only once `eda_review.md` is confirmed, invoke this skill's build stage (copy/symlink
   `skill.md` into `.claude/skills/churn-eda-profiling/` in your own repo per the discovery
   note at the end of `skill.md`, or paste its contents directly) to generate the verified
   analysis modules, notebook, scripts, tests, and documentation in one run.
6. Spot-check the outputs yourself per `Helper Guide.docx` before treating the build as done.

## Evidence to Submit

Place all of the following in `outputs/artifacts/` in your submission zip:
- `EDA_FINDINGS.md`
- `MODEL_RECOMMENDATION.md`
- `DATA_ISSUES.md`
- `ARTIFACT_NOTES.md`
- `review_log.md`
- Test run output/results (e.g. `pytest -v` output saved to a file, or a screenshot)
- Any spot-check evidence (e.g. your own hand-computed churn rate or hypothesis-test result)
  referenced in `Evaluation Rubric.xlsx`

## Notes for Evaluators

- Confirm `eda_review.md` reflects the learner's own judgment before the build, not a
  Claude-authored draft rubber-stamped after the fact.
- Confirm the leakage-circularity flag (days-since-last-transaction / trailing-90-day spend
  vs. the label's own definition) is named specifically, not just a generic "watch for
  leakage" caveat.
- Confirm `EDA_FINDINGS.md`'s numeric claims actually reproduce — `scripts/verify_findings.py`
  should run clean, and `test_findings_reproduce.py` should fail if a claim is deliberately
  corrupted.
- Confirm `MODEL_RECOMMENDATION.md` explicitly excludes or caveats any leakage-tainted
  variable rather than silently building a recommendation on top of it.
- Confirm the multi-source check (`transactions.db` vs.
  `transactions_monthly_agg.parquet`) actually reaggregates and compares month by month,
  rather than restating that they "could" disagree without checking.
