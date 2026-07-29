# Model Report

This report template explains how the landing prediction model should be evaluated and communicated. It is written as a consulting-style model report, with placeholders where final notebook or pipeline-generated metrics should be recorded.

## Modeling Objective

Predict whether a Falcon 9 first stage will land successfully using historical launch and mission attributes.

Problem type:

- Supervised learning.
- Binary classification.
- Target: landing success.

## Candidate Models

The reusable model layer supports the following classifiers:

| Model | Why It Is Included |
| --- | --- |
| Random Forest | Strong baseline for tabular data, handles nonlinear relationships, provides feature importance. |
| Gradient Boosting | Often strong on structured data, captures nonlinear interactions. |
| Logistic Regression | Interpretable linear baseline. |
| Support Vector Machine | Alternative classifier for margin-based decision boundaries. |

## Data Split and Reproducibility

Default configuration:

- Test size: `0.2`
- Random state: `42`
- Cross-validation folds: `5`

These defaults are defined in `src/config.py`.

## Metric Comparison

Record final model metrics here after running the modeling notebook or future pipeline.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Random Forest | TBD | TBD | TBD | TBD | TBD | Tree-based baseline. |
| Gradient Boosting | TBD | TBD | TBD | TBD | TBD | Candidate nonlinear model. |
| Logistic Regression | TBD | TBD | TBD | TBD | TBD | Interpretable baseline. |
| SVM | TBD | TBD | TBD | TBD | TBD | Margin-based classifier. |

## Recommended Model Selection Logic

Select the final model using these criteria:

1. F1 score for balanced classification quality.
2. Recall if the priority is identifying likely successful landings.
3. Precision if the priority is avoiding overconfident success predictions.
4. ROC-AUC for threshold-independent ranking quality.
5. Cross-validation stability.
6. Interpretability and simplicity when metrics are close.

The recommended model should not be selected by accuracy alone.

## Confusion Matrix Interpretation

The confusion matrix should be used to explain operational error types:

| Prediction Type | Meaning |
| --- | --- |
| True positive | Model predicts successful landing, and landing succeeds. |
| True negative | Model predicts unsuccessful landing, and landing does not succeed. |
| False positive | Model predicts success, but landing does not succeed. |
| False negative | Model predicts failure, but landing succeeds. |

Business interpretation:

- False positives can create overconfidence in recovery expectations.
- False negatives can underestimate viable successful landing profiles.

## Feature Importance Interpretation

For tree-based models, use `plot_feature_importance()` to communicate which variables are most influential.

Important cautions:

- Feature importance does not prove causality.
- Correlated variables can split importance.
- Encoded categorical variables should be interpreted back in business language.
- Final reports should explain top features in terms of launch context, not just column names.

## Error Analysis

A consulting-ready model report should inspect where the model fails:

- Which launch sites are associated with errors?
- Are high-payload launches harder to classify?
- Are older launches different from newer launches?
- Are specific orbit categories overrepresented in errors?
- Does the model perform differently across reused versus non-reused boosters?

## Model Risks

Known risks:

- Public/lab data may be incomplete.
- Historical launch patterns may not represent future launches.
- The model may learn correlations that are not causal.
- Final feature engineering choices can materially affect metrics.
- Small class counts can make metrics unstable.

## Recommendation

Until final pipeline metrics are stored, the repository should treat the selected model as provisional. The recommended next step is to add a reproducible training and evaluation pipeline that writes:

- `reports/metrics.json`
- `reports/model_config.json`
- confusion matrix figure
- feature-importance figure

Once those artifacts exist, this report should be updated with final values and a clear selected-model recommendation.
