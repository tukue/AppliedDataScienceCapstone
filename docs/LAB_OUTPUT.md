# Lab Output Guide

This guide describes the expected final lab output for reviewers and instructors.

## Output Standard

The lab output should be concise, reproducible, and free of local machine details.

Professional output includes:

- Clear section titles for data collection, preparation, EDA, modeling, and evaluation.
- Tables with meaningful column names and readable row counts.
- Graphs with descriptive titles, axis labels, legends, and consistent sizing.
- Model metrics reported as a compact dictionary or table.
- Saved artifacts referenced with project-relative paths such as `reports/metrics.json`.

The output should not include:

- Local usernames.
- Absolute folders from a developer machine.
- Temporary notebook kernel paths.
- Package installation logs.
- Warning tracebacks that are not part of the analysis.
- Console logging inside graph cells.

## Recommended Lab Narrative

The final notebook or report should follow this order:

1. Business question: predict Falcon 9 first-stage landing success.
2. Data sources: SpaceX API and preserved lab datasets.
3. Data quality checks: row counts, missing values, target balance, and feature availability.
4. Data preparation: missing-value handling, categorical encoding, and feature engineering.
5. Exploratory analysis: payload, orbit, launch site, reuse, and time-based patterns.
6. Modeling: train/test split, candidate classifiers, and reproducible random seed.
7. Evaluation: accuracy, precision, recall, F1, ROC-AUC, confusion matrix, and feature importance.
8. Conclusion: model interpretation, limitations, and next improvement steps.

## Clean Output Policy

Runtime logs are silent by default. When logs are explicitly enabled, file paths are shown in a reviewer-friendly format and should not expose local user folders.

Examples:

| Avoid | Use |
| --- | --- |
| Absolute local user paths | `data/raw/launches.csv` |
| Temporary notebook kernel paths | A short warning-free explanation |
| Long package installation output | Dependency list in `requirements.txt` |
| Graph cells with logs above figures | Figure plus caption or short interpretation |

## Graph Output Requirements

Each chart should be well-formed:

- Title states the analytical question.
- X and Y axes include human-readable labels.
- Categorical labels are readable and not clipped.
- Color is used consistently for outcome classes.
- Figure dimensions are stable across runs.
- Saved figures are high resolution and readable when opened outside the notebook.

## Reproducibility

Use the project commands below for clean local validation:

```bash
python -m src.pipeline
pytest -q
black --check src tests
flake8 src tests
```

Generated reports are written to `reports/`. Generated figures are written to `notebooks/figures/`. These outputs are intentionally ignored by Git so the repository stays clean.
