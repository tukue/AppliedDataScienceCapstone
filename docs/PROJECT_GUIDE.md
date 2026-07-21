# Project Guide

This guide explains the repository from the point of view of a reviewer, instructor, or data scientist who wants to understand the work quickly.

## Executive Summary

The project predicts Falcon 9 first-stage landing success from launch-related features. The work demonstrates a full applied data science workflow:

- Define a practical prediction problem.
- Collect and inspect SpaceX launch data.
- Prepare model-ready features.
- Explore patterns visually.
- Train and evaluate classification models.
- Communicate results through notebooks, reusable code, tests, and saved figures.

The original lab notebooks are preserved in `notebooks/original/`. The production-style implementation lives in `src/`.

## What Problem Is Being Solved?

The target is whether the first stage lands successfully after launch. In business terms, successful booster recovery can reduce launch cost and affects how a launch provider or analyst estimates mission economics.

This is a supervised binary classification problem:

- Positive class: successful landing.
- Negative class: failed or unsuccessful landing.

## What To Review First

Use this order when reviewing the repository:

1. `README.md`: project summary, structure, and setup.
2. `docs/METHODOLOGY.md`: full data science methodology.
3. `notebooks/original/`: preserved lab notebooks and outputs.
4. `src/data/`: API collection and data processing.
5. `src/features/`: graph output and feature engineering.
6. `src/models/`: model training and evaluation.
7. `tests/`: regression tests for data processing, features, logging, models, and visualization output.

## Notebook Map

| Notebook | Purpose |
| --- | --- |
| `jupyter-labs-spacex-data-collection-api.ipynb` | Collect SpaceX launch data from the API. |
| `labs-jupyter-spacex-Data-wrangling.ipynb` | Clean and prepare launch records. |
| `edadataviz.ipynb` | Explore launch patterns with visualizations. |
| `jupyter-labs-eda-sql-coursera_sqllite.ipynb` | Use SQL-style analysis for exploratory questions. |
| `lab_jupyter_launch_site_location.ipynb` | Explore launch-site geography and location context. |
| `SpaceX_Machine_Learning_Prediction_Part_5.ipynb` | Train and compare machine learning models. |
| `visualizing_stock_data.ipynb` | Preserved original visualization lab content. |
| `extracting_data_task.ipynb` | Preserved original data extraction lab content. |

Some notebooks have duplicate filenames with spaces and hyphens because the original lab exports are preserved as-is.

## Data Contract

The reusable code expects tabular launch data in pandas DataFrames.

Typical input columns include:

| Column Type | Examples | How It Is Used |
| --- | --- | --- |
| Launch metadata | flight number, date/time | Time trends and model features. |
| Payload information | payload mass | Main numeric predictor. |
| Mission context | orbit, launch site | Categorical predictors and group comparisons. |
| Booster/core information | booster version, core reuse | Engineering and model features. |
| Outcome | landing success/class | Target variable for classification. |

Runtime-generated data should stay in:

- `data/raw/` for unmodified source extracts.
- `data/processed/` for cleaned model-ready tables.
- `notebooks/figures/` for saved plots.
- `models/` for serialized model artifacts.

These artifacts are ignored by Git except for `.gitkeep` placeholders.

## Code Map

| Area | Main Files | Responsibility |
| --- | --- | --- |
| Configuration | `src/config.py` | Central paths, random seeds, and default model settings. |
| Logging | `src/logger.py` | Silent-by-default logging for clean notebook output. |
| Data collection | `src/data/__init__.py` | SpaceX API fetch helpers and raw CSV IO. |
| Data preparation | `src/data/processing.py` | Missing values, outliers, encoding, and scaling. |
| Visualization | `src/features/__init__.py` | Professional distribution, correlation, scatter, performance, and feature-importance charts. |
| Feature engineering | `src/features/engineering.py` | Datetime, interaction, polynomial, and feature-selection helpers. |
| Modeling | `src/models/__init__.py` | Train/test split, model fitting, evaluation, CV, tuning, save/load, and prediction. |

## Modeling Approach

The model layer supports four classifiers:

- Random Forest
- Gradient Boosting
- Logistic Regression
- Support Vector Machine

The recommended review path is:

1. Establish a simple baseline.
2. Train multiple candidate classifiers.
3. Compare metrics on the same train/test split.
4. Use cross-validation to check stability.
5. Tune the best candidate only after baseline comparison.
6. Interpret the model with confusion matrices and feature-importance plots where supported.

## Evaluation Guide

For this binary classification problem:

- Accuracy answers: how often is the model correct overall?
- Precision answers: when the model predicts success, how often is it right?
- Recall answers: how many actual successes does the model identify?
- F1 balances precision and recall.
- ROC-AUC measures ranking quality across thresholds.
- Confusion matrix shows false positives and false negatives.
- Feature importance helps explain which variables drive tree-based models.

Do not rely on a single metric. A good lab output should explain the tradeoff between false positives and false negatives.

## Reproducibility Notes

The code uses:

- `RANDOM_STATE = 42`
- `TEST_SIZE = 0.2`
- `CV_FOLDS = 5`

Tests are designed to protect against common regressions:

- Deprecated pandas API usage.
- DataFrame mutation side effects.
- Noisy log output in notebooks.
- Malformed or unreadable saved graph files.
- Model save/load failures.

## Known Scope

This is a learning project, not a production forecasting service. The purpose is to demonstrate applied data science methodology, clean project organization, and reproducible model-development practices.
