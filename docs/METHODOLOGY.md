# Data Science Methodology

This project follows the standard applied data science workflow used in the IBM Applied Data Science Capstone. The goal is to move from a real business question to a tested model and clear lab output.

## 1. Business Understanding

The business question is whether a SpaceX Falcon 9 first stage will land successfully after launch.

This matters because booster recovery affects launch cost. A model that estimates landing success can support cost estimation, launch comparison, and risk discussion.

Project objective:

- Predict the binary landing outcome for Falcon 9 launches.
- Identify the variables most associated with successful landings.
- Present results in notebooks, reusable code, and professional visual outputs.

## 2. Data Collection

The lab collects and preserves data from multiple sources:

- SpaceX REST API launch records.
- Rocket, core, payload, and launch-site attributes.
- Original Coursera notebooks and lab outputs in `notebooks/original/`.

The refactored code keeps data collection reusable through `src.data`, with raw outputs stored under `data/raw/` when generated locally.

## 3. Data Understanding

The analysis inspects the available launch records before modeling:

- Number of launches and landing outcomes.
- Missing values and incomplete fields.
- Payload mass, orbit, launch site, booster version, and flight-number patterns.
- Relationships between candidate predictors and landing success.

This step is supported by the original notebooks and the plotting helpers in `src.features`.

## 4. Data Preparation

The project prepares data before modeling by:

- Handling missing values with documented strategies.
- Encoding categorical variables for model compatibility.
- Normalizing numeric features where needed.
- Creating datetime, interaction, and polynomial features.
- Separating raw, processed, external, model, log, and figure artifacts into dedicated directories.

Preparation code is modularized in `src.data.processing` and `src.features.engineering` so the work can be reused outside notebooks.

## 5. Exploratory Data Analysis

EDA is used to understand patterns before fitting models. The lab output includes:

- Distribution charts for launch and payload variables.
- Correlation heatmaps for numeric predictors.
- Scatter plots for feature relationships.
- Categorical outcome comparisons by launch site, orbit, or other groups.

The visualization utilities produce high-resolution, presentation-ready charts saved under `notebooks/figures/`.

## 6. Modeling

The prediction task is treated as supervised binary classification. The model workflow includes:

- Train/test splitting with a fixed random seed for reproducibility.
- Baseline model training.
- Multiple candidate algorithms:
  - Random Forest
  - Gradient Boosting
  - Logistic Regression
  - Support Vector Machine
- Cross-validation.
- Hyperparameter tuning with grid search where appropriate.

Reusable model logic lives in `src.models.ModelTrainer`.

## 7. Evaluation

Models are evaluated with metrics that match a classification problem:

- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Cross-validation mean and standard deviation
- Confusion matrix
- Feature importance for interpretable models

The project includes professional graph output for confusion matrices, residual-style diagnostic plots, and ranked feature importance.

## 8. Communication and Reproducibility

The final lab output is designed to be reviewable and reproducible:

- Original notebooks remain unchanged in `notebooks/original/`.
- Reusable source code is organized under `src/`.
- Tests validate data, model, and visualization behavior.
- CI checks formatting, linting, tests, documentation, and packaging.
- Documentation explains setup, API usage, methodology, and development workflow.

This structure keeps the educational notebook outputs intact while making the project easier to run, inspect, test, and extend.
