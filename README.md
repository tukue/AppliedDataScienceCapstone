# SpaceX Falcon 9 Landing Prediction

[![Tests & Code Quality](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/tests.yml/badge.svg)](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/tests.yml)
[![Documentation](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/docs.yml/badge.svg)](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/docs.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Applied Data Science Capstone project for predicting whether a SpaceX Falcon 9 first stage will land successfully. The original Coursera lab notebooks are preserved, and reusable Python modules have been added for data collection, cleaning, visualization, feature engineering, model training, and evaluation.

## Lab Outcome

The repository is organized so a reviewer can see both the original lab work and the engineering improvements:

- Original notebooks remain in `notebooks/original/` with their embedded outputs.
- Reusable code lives in `src/` and is covered by tests in `tests/`.
- Runtime artifacts are separated into `data/`, `models/`, `logs/`, and `notebooks/figures/`.
- CI validates tests, formatting, linting, package build, and documentation structure.

## Project Structure

```text
AppliedDataScienceCapstone/
|-- .github/workflows/          # GitHub Actions workflows
|-- data/
|   |-- external/               # External data sources
|   |-- processed/              # Cleaned and transformed data
|   `-- raw/                    # Raw API/source data
|-- docs/                       # API, methodology, and CI/CD documentation
|-- logs/                       # Runtime logs
|-- models/                     # Trained model artifacts
|-- notebooks/
|   |-- figures/                # Saved plots and figures
|   `-- original/               # Preserved capstone notebooks
|-- src/
|   |-- config.py               # Project paths and constants
|   |-- logger.py               # Logging setup
|   |-- data/                   # Data collection and processing
|   |-- features/               # Visualization and feature engineering
|   `-- models/                 # Model training and evaluation
|-- tests/                      # Unit tests
|-- .env.example                # Example environment variables
|-- pyproject.toml              # Tool configuration
|-- requirements.txt            # Runtime dependencies
|-- requirements-dev.txt        # Development dependencies
`-- setup.py                    # Package metadata
```

## Data Science Methodology

The lab follows a practical end-to-end data science methodology:

1. Business understanding: define the prediction objective as estimating Falcon 9 first-stage landing success.
2. Data collection: gather launch, rocket, core, payload, and site data from the SpaceX API and provided lab sources.
3. Data understanding: inspect records, missing values, feature distributions, launch outcomes, and relationships between variables.
4. Data preparation: clean missing values, encode categorical fields, create reusable features, and separate raw data from processed data.
5. Exploratory analysis: compare payload mass, orbit, launch site, flight number, and landing outcomes with professional charts.
6. Modeling: train classification models including Random Forest, Gradient Boosting, Logistic Regression, and SVM.
7. Evaluation: compare accuracy, precision, recall, F1, ROC-AUC, cross-validation scores, confusion matrices, and feature importance.
8. Communication and reproducibility: preserve notebooks, save figures and models, document the workflow, and validate code through tests and CI.

See [Data Science Methodology](docs/METHODOLOGY.md) for the detailed process followed by the lab.

## Quick Start

```bash
git clone git@github.com:tukue/AppliedDataScienceCapstone.git
cd AppliedDataScienceCapstone

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pytest
```

Open the original notebooks:

```bash
jupyter notebook notebooks/original/
```

## Programmatic Usage

```python
from src.data import fetch_spacex_launches, save_raw_data
from src.data.processing import encode_categorical, handle_missing_values
from src.features import plot_distribution, save_figure
from src.models import ModelTrainer

launches = fetch_spacex_launches()
save_raw_data(launches, "spacex_launches.csv")

clean = handle_missing_values(launches, strategy="mean")
clean = encode_categorical(clean, ["site_name"], method="onehot")

trainer = ModelTrainer(model_type="random_forest")
X_train, X_test, y_train, y_test = trainer.split_data(X, y)
trainer.train(X_train, y_train)
metrics = trainer.evaluate(X_test, y_test)

fig = plot_distribution(clean, "payload_mass_kg")
save_figure(fig, "payload_distribution.png")
print(metrics)
```

## Core Modules

`src.data`

- Fetch SpaceX launch, rocket, and core data from the SpaceX REST API.
- Save and load raw CSV files under `data/raw/`.

`src.data.processing`

- Handle missing values with drop, mean, median, or forward-fill strategies.
- Remove outliers with the IQR method.
- Encode categorical variables and normalize numeric features.

`src.features`

- Create presentation-ready distribution, correlation, scatter, categorical, and model-performance plots.
- Create ranked feature-importance plots for model interpretation.
- Save high-resolution generated figures under `notebooks/figures/`.

`src.features.engineering`

- Create datetime features.
- Create interaction and polynomial features.
- Select features using mutual information, correlation, or variance.

`src.models`

- Train Random Forest, Gradient Boosting, Logistic Regression, and SVM classifiers.
- Split data, run cross-validation, tune hyperparameters, evaluate metrics, and save models.

## Development Workflow

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the local quality checks:

```bash
pytest
black --check src tests
flake8 src tests
mypy src --ignore-missing-imports
```

Format code before committing:

```bash
black src tests
```

## Reproducibility

- Default random seed: `42`
- Default test split: `0.2`
- Default cross-validation folds: `5`
- Runtime data, logs, figures, and model binaries are not committed.
- Empty artifact directories are tracked with `.gitkeep` so examples work after a fresh clone.

Copy `.env.example` to `.env` if you need local overrides:

```bash
cp .env.example .env
```

## Documentation

- [Quick Start](QUICKSTART.md)
- [Data Science Methodology](docs/METHODOLOGY.md)
- [API Reference](docs/API.md)
- [CI/CD Guide](docs/CICD.md)
- [CI/CD Setup](docs/CICD_SETUP.md)
- [Contributing](CONTRIBUTING.md)
- [Refactoring Summary](REFACTORING_COMPLETE.md)
- [Detailed Refactoring Notes](PROJECT_REFACTORING.md)

## Preserved Lab Work

All original notebooks are kept in `notebooks/original/`. The refactored package is additive: it does not overwrite the submitted lab notebooks or their embedded visual outputs.

## Disclaimer

This is a learning project for data science methodology and model evaluation. SpaceX data is used as a public learning dataset; this project is not affiliated with SpaceX.

## References

- [SpaceX API Documentation](https://docs.spacexdata.com/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/)
