# SpaceX Falcon 9 Landing Prediction - Applied Data Science Capstone

[![Tests & Code Quality](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/tests.yml/badge.svg)](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/tests.yml)
[![Documentation](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/docs.yml/badge.svg)](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/docs.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive machine learning project following data science best practices for predicting SpaceX Falcon 9 booster landing success.

## Project Overview

This project demonstrates the complete data science methodology:
- **Data Collection**: Using SpaceX REST API
- **Data Wrangling**: Cleaning and preprocessing
- **Exploratory Data Analysis (EDA)**: Understanding data patterns
- **Data Visualization**: Creating insightful visualizations
- **Feature Engineering**: Creating predictive features
- **Model Development**: Training multiple models
- **Model Evaluation**: Assessing performance
- **Reporting**: Presenting results to stakeholders

## Project Structure

```
AppliedDataScienceCapstone/
├── data/                          # Data directory
│   ├── raw/                      # Raw data from API/sources
│   ├── processed/                # Processed and cleaned data
│   └── external/                 # External data sources
├── notebooks/                     # Jupyter notebooks
│   ├── original/                 # Original capstone notebooks (preserved with all graphs)
│   ├── exploratory/              # Refactored analysis notebooks
│   └── figures/                  # Generated plots and visualizations
├── src/                          # Source code modules
│   ├── config.py                # Configuration and paths
│   ├── logger.py                # Logging setup
│   ├── data/                    # Data loading and processing
│   │   ├── __init__.py         # Data collection utilities
│   │   └── processing.py       # Data cleaning and transformation
│   ├── features/               # Feature engineering
│   │   ├── __init__.py        # Visualization utilities
│   │   └── engineering.py     # Feature creation
│   └── models/                # Model training and evaluation
│       └── __init__.py        # ModelTrainer class
├── tests/                       # Unit tests
├── models/                      # Trained model artifacts
├── logs/                        # Application logs
├── docs/                        # Documentation
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. Clone the repository:
```bash
git clone git@github.com:tukue/AppliedDataScienceCapstone.git
cd AppliedDataScienceCapstone
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Usage

### Viewing Original Analysis

All original notebooks with generated graphs and visualizations are preserved:
```bash
jupyter notebook notebooks/original/
```

**Key Original Notebooks:**
- `jupyter-labs-spacex-data-collection-api.ipynb` - SpaceX API data collection
- `labs-jupyter-spacex-Data-wrangling.ipynb` - Data cleaning and wrangling
- `edadataviz.ipynb` - Exploratory data analysis
- `SpaceX_Machine_Learning_Prediction_Part_5.ipynb` - Machine learning models
- `visualizing_stock_data.ipynb` - Advanced visualization techniques

### Using Refactored Modular Code

Refactored notebooks using the new modular structure:
```bash
jupyter notebook notebooks/exploratory/
```

### Programmatic Usage

```python
from src.data import fetch_spacex_launches, save_raw_data
from src.data.processing import handle_missing_values, encode_categorical
from src.features import plot_distribution, save_figure
from src.models import ModelTrainer

# Load data from SpaceX API
launches_df = fetch_spacex_launches()
save_raw_data(launches_df, 'spacex_launches.csv')

# Process data
launches_df = handle_missing_values(launches_df, strategy='mean')
launches_df = encode_categorical(launches_df, ['site_name'], method='onehot')

# Train model
trainer = ModelTrainer(model_type='random_forest')
X_train, X_test, y_train, y_test = trainer.split_data(X, y)
trainer.train(X_train, y_train)
metrics = trainer.evaluate(X_test, y_test)
print(f"Model Accuracy: {metrics['accuracy']:.4f}")

# Visualize results
fig = plot_distribution(launches_df, 'payload_mass_kg')
save_figure(fig, 'payload_distribution.png')
```

## Module Features

### Data Module (`src/data/`)
- SpaceX API data collection (launches, rockets, cores)
- CSV data loading and saving
- Missing value handling (drop, mean, median, forward fill)
- Outlier detection using IQR method
- Categorical encoding (one-hot, label)
- Feature normalization (standard, min-max)

### Features Module (`src/features/`)
- Distribution plots and visualizations
- Correlation matrix heatmaps
- Scatter plots and categorical analysis
- DateTime feature extraction
- Interaction features
- Polynomial features
- Feature selection (mutual info, correlation, variance)

### Models Module (`src/models/`)
- Multiple algorithms (Random Forest, Gradient Boost, Logistic Regression, SVM)
- Train-test split with configurable ratios
- Cross-validation (k-fold)
- Hyperparameter tuning (GridSearchCV)
- Model evaluation (accuracy, precision, recall, F1, ROC-AUC)
- Model persistence (save/load)

### Configuration (`src/config.py`)
- Centralized project paths
- Data directories configuration
- Model hyperparameters
- Logging configuration

## Best Practices Implemented

✅ **Project Organization**: Standard data science directory structure  
✅ **Modularity**: Reusable functions in separate modules  
✅ **Configuration Management**: Centralized config with environment support  
✅ **Logging**: Structured logging throughout the project  
✅ **Documentation**: Comprehensive docstrings and README  
✅ **Version Control**: Proper .gitignore for clean repositories  
✅ **Dependency Management**: Pinned versions for reproducibility  
✅ **Data Lifecycle**: Separate raw, processed, and external data dirs  
✅ **Artifact Management**: Separate directories for models, logs, and figures  
✅ **Testing**: Test directory structure ready for unit tests  
✅ **Preserved Outputs**: All original graphs and notebooks intact  

## Preserved Content

All original work is fully preserved:
- ✅ All 10 original `.ipynb` files in `notebooks/original/`
- ✅ All generated visualizations and graphs embedded in notebooks
- ✅ All data outputs from original analysis
- ✅ Complete analysis history and methodologies
- ✅ Original data processing workflow

New additions don't overwrite or modify original notebooks.

## Development

### Continuous Integration

This project uses **GitHub Actions** for automated testing and code quality checks:

- ✅ **Automated Tests** - 12+ test cases run on every push
- ✅ **Code Quality** - Black formatting, Flake8 linting, mypy type checking
- ✅ **Security** - Bandit security scan, dependency vulnerability checks
- ✅ **Coverage** - Test coverage reports uploaded to Codecov
- ✅ **Documentation** - API documentation validation

See [docs/CICD.md](docs/CICD.md) for detailed CI/CD documentation.

### Run Tests Locally

```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

Run with coverage:
```bash
pytest --cov=src tests/
```

Format code with Black:
```bash
black src/ tests/
```

Lint code with Flake8:
```bash
flake8 src/ tests/
```

Type check with mypy:
```bash
mypy src/
```

## Disclaimer

This is a learning project. The SpaceX data is used as a learning dataset to demonstrate data science methodology for model development and evaluation. The developer has no affiliation with SpaceX.

## References

- [SpaceX API Documentation](https://docs.spacexdata.com/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Cookiecutter Data Science](https://cookiecutter-data-science.readthedocs.io/)

---

**Last Updated**: July 2026  
**Status**: Refactored with best practices while preserving original content  
**Version**: 2.0 (Improved Structure & Modularity)
