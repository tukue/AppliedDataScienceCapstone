# Executive Summary

## Business Question

Can we estimate whether a SpaceX Falcon 9 first stage will land successfully using historical launch, payload, orbit, and launch-site information?

Booster recovery is important because a successful landing can materially reduce launch economics. A model that estimates landing success helps frame mission risk, compare launch profiles, and communicate the drivers of successful recovery.

## Project Objective

The project is a supervised binary classification analysis:

- Target: first-stage landing success.
- Inputs: launch metadata, payload information, orbit, launch site, booster/core attributes, and engineered features.
- Output: model predictions, evaluation metrics, and interpretation artifacts.

## Data Used

The analysis uses SpaceX launch-related data from the original capstone labs and SpaceX API workflows. The original notebooks are preserved in `notebooks/original/`, while reusable source code is organized under `src/`.

Primary data themes:

- Launch timing and flight number.
- Launch site and orbit.
- Payload mass.
- Booster/core metadata.
- Landing outcome.

## Analytical Approach

The project follows an end-to-end data science methodology:

1. Define the business problem.
2. Collect SpaceX launch data.
3. Inspect data quality and feature distributions.
4. Prepare model-ready features.
5. Explore relationships through visual analysis.
6. Train candidate classification models.
7. Evaluate model performance.
8. Communicate findings with documentation and figures.

## Current Deliverables

The repository currently provides:

- Preserved original notebooks with lab outputs.
- Reusable data processing, feature engineering, visualization, and modeling modules.
- Professional graph output helpers.
- Silent-by-default logging for clean notebooks.
- Regression tests for data processing, feature engineering, visualization, logging, and model behavior.
- Reviewer-oriented documentation.

## Recommended Model Decision

The model recommendation should be based on the final metric comparison in the modeling notebook or future pipeline output.

Recommended selection criteria:

- Strong F1 score for balanced precision and recall.
- Acceptable recall if missing successful landings is costly.
- Acceptable precision if false success predictions are risky.
- Stable cross-validation results.
- Interpretability through feature importance when possible.

If multiple models perform similarly, prefer the simpler or more interpretable model unless there is a clear performance benefit from a more complex model.

## Business Interpretation

The key business value is not only the prediction but also the explanation of which launch characteristics are associated with landing success. Feature importance, categorical outcome comparisons, and confusion matrices should be used to explain:

- Which launch profiles are associated with better recovery outcomes.
- Where the model is most uncertain.
- Which errors matter most for decision-making.

## Risks and Limitations

Important limitations:

- The project is a learning capstone, not an operational launch-risk system.
- Historical data may not represent future launch conditions.
- Public/lab data can be incomplete or simplified.
- Model performance depends on final feature selection and data preparation.
- False positives and false negatives have different business meanings and should be discussed explicitly.

## Recommended Next Steps

1. Add a reproducible pipeline that runs data preparation, model training, and evaluation end to end.
2. Store final metrics in `reports/metrics.json`.
3. Add a final model report with selected model, metrics, confusion matrix, and feature importance.
4. Add data validation checks before modeling.
5. Add a clean final notebook or report for stakeholder presentation.

## Stakeholder Takeaway

This repository now provides a clear foundation for a client-ready data science deliverable. The next step is to connect the reusable code to a repeatable pipeline and final report so the model result can be audited without manually inspecting every notebook.
