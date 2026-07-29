# Improvement Plan

This plan describes the next upgrades that would make the repository stronger as a data science consulting deliverable. It is intentionally prioritized so work can be implemented in small, reviewable increments.

## Current State

The repository already has a solid foundation:

- Original capstone notebooks are preserved.
- Reusable source code exists for data collection, processing, feature engineering, visualization, and modeling.
- Tests cover data processing, feature engineering, logging, model behavior, and graph output.
- Documentation explains the project methodology and reviewer path.
- Graph output is styled for professional lab reporting.

The next phase should focus on turning the project from a refactored capstone into a client-ready analytical product.

## Priority 1: Consulting Deliverables

### 1. Executive Summary

Status: implemented in `docs/EXECUTIVE_SUMMARY.md`.

Create `docs/EXECUTIVE_SUMMARY.md`.

Purpose:

- Explain the project in business language.
- Summarize the analytical question, model result, risks, and recommendations.
- Make the repository understandable to non-technical stakeholders.

Recommended sections:

- Business question
- Data used
- Key findings
- Recommended model
- Business interpretation
- Limitations
- Next steps

Expected impact:

- Improves stakeholder readability.
- Makes the project feel like a consulting engagement, not just a code repository.

### 2. Final Model Report

Status: implemented as a consulting report template in `docs/MODEL_REPORT.md`.

Create `docs/MODEL_REPORT.md`.

Purpose:

- Explain how models were evaluated and compared.
- Show the selected model and why it was selected.

Recommended sections:

- Modeling objective
- Train/test split
- Candidate models
- Metric comparison table
- Confusion matrix interpretation
- Feature importance interpretation
- Error analysis
- Final recommendation

Expected impact:

- Makes the model decision auditable.
- Helps reviewers understand tradeoffs between precision, recall, F1, and ROC-AUC.

### 3. Data Dictionary

Status: implemented in `docs/DATA_DICTIONARY.md`.

Create `docs/DATA_DICTIONARY.md`.

Purpose:

- Document the meaning and expected type of important fields.
- Clarify which fields are source data, engineered features, or model targets.

Recommended columns:

| Field | Type | Source | Nullable | Used In Model | Description |
| --- | --- | --- | --- | --- | --- |
| `payload_mass_kg` | numeric | SpaceX/API/lab | yes | yes | Payload mass for the launch. |
| `orbit` | categorical | SpaceX/API/lab | yes | yes | Target orbit category. |
| `launch_site` | categorical | SpaceX/API/lab | yes | yes | Launch site identifier. |
| `landing_success` | binary | derived/lab | no | target | Whether the first stage landed successfully. |

Expected impact:

- Reduces ambiguity for future maintainers.
- Supports reproducibility and data validation.

## Priority 2: Reproducible Pipeline

### 4. Pipeline Entry Point

Status: implemented as `python -m src.pipeline` with deterministic sample launch data.

Add a runnable pipeline, for example:

```bash
python -m src.pipeline
```

Or split it into smaller commands:

```bash
python -m src.pipeline.collect
python -m src.pipeline.prepare
python -m src.pipeline.train
python -m src.pipeline.evaluate
```

Purpose:

- Make the full workflow executable outside notebooks.
- Reduce manual steps for reviewers and future contributors.

Expected outputs:

- Raw data in `data/raw/`
- Processed data in `data/processed/`
- Model artifact in `models/`
- Metrics in `reports/metrics.json`
- Figures in `notebooks/figures/` or `reports/figures/`

Expected impact:

- Makes the project reproducible end to end.
- Creates a clear path from source data to final model output.

### 5. Task Runner

Status: implemented with `Makefile` targets for install, test, lint, format, and run.

Add a `Makefile` or equivalent task runner.

Recommended commands:

```makefile
install:
	pip install -r requirements-dev.txt

test:
	pytest

lint:
	black --check src tests
	flake8 src tests

format:
	black src tests

run:
	python -m src.pipeline
```

Expected impact:

- Makes common actions discoverable.
- Reduces onboarding friction.

## Priority 3: Data Quality and Validation

### 6. Data Validation Module

Status: implemented in `src/data/validation.py`.

Add `src/data/validation.py`.

Purpose:

- Fail early when data is missing required fields or has invalid values.
- Make assumptions explicit before modeling.

Recommended checks:

- Required columns exist.
- Target is binary.
- Numeric columns contain numeric values.
- Null rates are below configurable thresholds.
- Payload mass is non-negative.
- Train/test features do not include the target column.

Expected impact:

- Prevents silent data-quality failures.
- Improves trust in the modeling workflow.

### 7. Validation Tests

Status: implemented in `tests/test_validation.py`.

Add `tests/test_validation.py`.

Recommended test cases:

- Missing required column raises `ValueError`.
- Non-binary target raises `ValueError`.
- Negative payload mass raises `ValueError`.
- Valid DataFrame passes all checks.

Expected impact:

- Protects assumptions as the project evolves.

## Priority 4: Experiment Tracking

### 8. Metrics Artifact

Status: implemented for the sample pipeline as `reports/metrics.json`.

Save model metrics to a structured file:

```text
reports/metrics.json
```

Example:

```json
{
  "model_type": "random_forest",
  "accuracy": 0.84,
  "precision": 0.82,
  "recall": 0.80,
  "f1": 0.81,
  "roc_auc": 0.88,
  "random_state": 42
}
```

Expected impact:

- Makes model results inspectable without rerunning notebooks.
- Supports comparison across model runs.

### 9. Model Configuration Artifact

Status: implemented for the sample pipeline as `reports/model_config.json`.

Save run configuration to:

```text
reports/model_config.json
```

Include:

- Model type
- Hyperparameters
- Feature columns
- Target column
- Split size
- Random seed

Expected impact:

- Improves reproducibility.
- Makes model outputs easier to audit.

## Priority 5: Notebook Organization

### 10. Clean Notebook Path

Keep `notebooks/original/` unchanged, but add a clean sequence for reviewers:

```text
notebooks/
|-- original/
|-- 01_data_collection.ipynb
|-- 02_data_wrangling.ipynb
|-- 03_eda.ipynb
|-- 04_modeling.ipynb
`-- 05_final_report.ipynb
```

Purpose:

- Preserve the lab evidence.
- Provide a cleaner walkthrough for future readers.

Expected impact:

- Easier review.
- Clearer separation between original coursework and polished analysis.

## Priority 6: Packaging and Naming

### 11. Rename Internal Package

Consider replacing generic `src` imports with a domain package:

```text
spacex_landing/
|-- data/
|-- features/
|-- models/
`-- visualization/
```

Expected impact:

- More professional package identity.
- Easier imports for users and maintainers.

Tradeoff:

- Requires import updates across source, tests, and docs.
- Should be done only after current PRs are stable.

## Suggested Implementation Order

1. Add `docs/EXECUTIVE_SUMMARY.md`.
2. Add `docs/DATA_DICTIONARY.md`.
3. Add `docs/MODEL_REPORT.md`.
4. Add `src/data/validation.py` and tests.
5. Add a simple pipeline entry point.
6. Add metrics/config artifacts under `reports/`.
7. Add clean reviewer notebooks.
8. Consider internal package rename.

## Definition of Done

Each improvement should include:

- Documentation update.
- Focused tests where code behavior changes.
- No mutation of caller-owned DataFrames unless explicitly documented.
- Clean graph or report output with no noisy logs.
- Passing checks:

```bash
pytest
black --check src tests
flake8 src tests
```

## Expected Result

After these improvements, the repository will read like a professional consulting project:

- Clear business framing.
- Clear data contract.
- Reproducible pipeline.
- Auditable model output.
- Strong tests and validation.
- Stakeholder-ready reports and figures.
