# Quick Start

Use this guide to run the lab, inspect the original outputs, and validate the refactored package.

For the full project workflow, see [Data Science Methodology](docs/METHODOLOGY.md). It explains how the lab moves from business understanding through data collection, preparation, EDA, modeling, evaluation, and communication.

## 1. Set Up the Environment

```bash
git clone git@github.com:tukue/AppliedDataScienceCapstone.git
cd AppliedDataScienceCapstone

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

## 2. View the Original Lab Notebooks

```bash
jupyter notebook notebooks/original/
```

The original notebooks are preserved with embedded charts and outputs. Start with:

- `jupyter-labs-spacex-data-collection-api.ipynb`
- `labs-jupyter-spacex-Data-wrangling.ipynb`
- `edadataviz.ipynb`
- `jupyter-labs-eda-sql-coursera_sqllite.ipynb`
- `lab_jupyter_launch_site_location.ipynb`
- `SpaceX_Machine_Learning_Prediction_Part_5.ipynb`

## 3. Run the Test Suite

```bash
pytest
```

Run coverage when you want a fuller local check:

```bash
pytest --cov=src --cov-report=term-missing
```

## 4. Common Tasks

### Load and Process Data

```python
from src.data import fetch_spacex_launches, load_raw_data, save_raw_data
from src.data.processing import encode_categorical, handle_missing_values

launches = fetch_spacex_launches()
save_raw_data(launches, "launches.csv")

launches = load_raw_data("launches.csv")
launches = handle_missing_values(launches, strategy="mean")
launches = encode_categorical(launches, ["site"], method="onehot")
```

### Visualize Data

```python
from src.features import plot_correlation_matrix, plot_distribution, save_figure

fig1 = plot_distribution(launches, "payload_mass_kg")
fig2 = plot_correlation_matrix(launches)

save_figure(fig1, "payload_distribution.png")
save_figure(fig2, "correlation_matrix.png")
```

Figures are saved at high resolution with a consistent presentation style for lab reports and review output.

For model interpretation:

```python
from src.features import plot_feature_importance, save_figure

feature_fig = plot_feature_importance(X.columns, trainer.model.feature_importances_)
save_figure(feature_fig, "feature_importance.png")
```

### Train and Evaluate a Model

```python
from src.models import ModelTrainer

trainer = ModelTrainer(model_type="random_forest")
X_train, X_test, y_train, y_test = trainer.split_data(X, y)

trainer.train(X_train, y_train)
metrics = trainer.evaluate(X_test, y_test)

print(f"Accuracy: {metrics['accuracy']:.4f}")
print(f"F1: {metrics['f1']:.4f}")

trainer.save_model("random_forest.pkl")
```

### Run Cross-Validation and Tuning

```python
cv_results = trainer.cross_validate(X, y, cv=5)
print(f"CV F1: {cv_results['cv_mean']:.4f}")

param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [5, 10, 15],
}
trainer.hyperparameter_tune(X_train, y_train, param_grid, cv=5)
trainer.save_model("random_forest_tuned.pkl")
```

### Create Features

```python
from src.features.engineering import (
    create_datetime_features,
    create_interaction_features,
    select_top_features,
)

df = create_datetime_features(df, "launch_date")
df = create_interaction_features(df, [("payload_mass_kg", "flight_number")])

top_features = select_top_features(X, y, method="mutual_info", n_features=10)
print(top_features)
```

## 5. File Locations

| Type | Location |
| --- | --- |
| Original notebooks | `notebooks/original/` |
| Saved figures | `notebooks/figures/` |
| Raw data | `data/raw/` |
| Processed data | `data/processed/` |
| External data | `data/external/` |
| Models | `models/` |
| Logs | `logs/` |
| Source code | `src/` |
| Tests | `tests/` |
| Documentation | `docs/` |

## 6. Quality Checks

```bash
black --check src tests
flake8 src tests
mypy src --ignore-missing-imports
```

Use `black src tests` to apply formatting.

## Troubleshooting

Import errors usually mean the virtual environment is inactive or dependencies are missing. Activate the environment and reinstall:

```bash
pip install -r requirements-dev.txt
```

API failures usually mean the SpaceX API or your network is unavailable. The original notebooks remain available for reviewing the completed lab outputs.
