# Starter Code — Churn EDA & Model-Family Recommendation

This is scaffolding, not a solution. Every file under `eda/`, `scripts/`, and `tests/`
contains function signatures, docstrings, and `TODO`s only — no working implementation.
`notebooks/eda_churn.ipynb` ships with section headers and `raise NotImplementedError`
placeholder cells only. `eda_review.md` is the one exception worth calling out explicitly:
it ships as **headers only**, with `<<LEARNER: ...>>` prompts instead of content — not
because it's less important, but because filling it in is the one part of this assignment
that's entirely your own judgment call, not Claude's. You do this by correcting Claude's
Stage 0-generated first-pass notebook and draft findings against `skill.md`'s Domain Context
section. See "What fills this in" below.

## How this relates to `skills/churn-eda-profiling/skill.md`

`skill.md` is the build spec Claude follows once your `eda_review.md` is confirmed. The
folder layout and function signatures in this scaffolding (`eda/load.py`'s three loaders,
`eda/profile.py`'s `profile_schema`/`profile_missingness`/`count_zero_activity_customers`/
`profile_distribution`/`count_outliers`, `eda/hypotheses.py`'s per-driver functions,
`eda/time_checks.py`'s `monthly_volume_trend`/`compare_row_level_vs_monthly_agg`,
`eda/leakage_checks.py`'s `flag_label_circular_drivers`/`check_no_post_as_of_rows_used`)
match exactly what `skill.md`'s Workflow section and its "Repo scaffold to create" specify —
this scaffold is the shape Claude fills in at the same paths, not a different or relocated
design. When you invoke the skill, Claude fills in these same files in place; it does not
create a parallel structure elsewhere.

## What fills this in

Claude (invoked via the `churn-eda-profiling` skill's Stage 0, to generate a first-pass EDA
notebook and draft findings from the raw sources), then you (correcting those drafts into
`eda_review.md` against `skill.md`'s Domain Context section, replacing every
`<<LEARNER: ...>>` prompt in the skeleton), then Claude again (invoked via the same skill's
build stage once your corrected review is confirmed) fill in:

- `eda_review.md` — **you**, alone, by correcting Stage 0's drafts — not Claude, and not a
  blank page either. The content under each heading is entirely your own judgment to decide,
  even where it ends up agreeing with Stage 0's original draft.
- `eda/` — loaders (`load.py`), profiling (`profile.py`), hypothesis tests (`hypotheses.py`),
  time/multi-source diagnostics (`time_checks.py`), leakage checks (`leakage_checks.py`)
- `scripts/` — the profiling, hypothesis-test, time/leakage-check, and findings-verification
  entry points
- `notebooks/eda_churn.ipynb` — the narrative version of the same analysis, runnable top to
  bottom
- `tests/` — the real test suite (this scaffold only has skipped test stubs)

Claude also generates `EDA_FINDINGS.md`, `MODEL_RECOMMENDATION.md`, `DATA_ISSUES.md`,
`ARTIFACT_NOTES.md`, and `review_log.md` at the repo root, per `skill.md`.

See `Assignment Document.docx`, `Helper Guide.docx`, and
`skills/churn-eda-profiling/skill.md` for the full sequence.

## Layout

```
starter-code/
  eda_review.md       headers only — <<LEARNER: ...>> prompts, yours to fill in before Claude sees it
  eda/                load.py, profile.py, hypotheses.py, time_checks.py, leakage_checks.py
  notebooks/          eda_churn.ipynb
  scripts/            run_profile.py, run_hypothesis_tests.py, run_time_and_leakage_checks.py, verify_findings.py
  tests/              test_load.py, test_profile.py, test_hypotheses.py, test_time_and_leakage_checks.py, test_findings_reproduce.py
  outputs/artifacts/  generated reports/logs/screenshots go here, not in eda/, scripts/, or tests/
  requirements.txt
  pytest.ini          sets pythonpath so `pytest` resolves eda/ imports with no extra flags
  .env.example
```

This mirrors `skill.md`'s "Repo scaffold to create" exactly (the raw data files and
`requirements.txt` also live at this same repo root once you bring them in during setup — see
`Helper Guide.docx`'s setup steps. `eda_review.md` is the one file already provided here as a
skeleton, not something you create from a blank file).
