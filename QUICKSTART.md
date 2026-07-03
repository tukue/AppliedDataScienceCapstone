# Quick Start Guide 🚀

## 5-Minute Setup

### 1. Clone & Setup
```bash
git clone git@github.com:tukue/AppliedDataScienceCapstone.git
cd AppliedDataScienceCapstone
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. View Original Notebooks
```bash
jupyter notebook notebooks/original/
```
All 10 original notebooks with graphs are here!

### 3. Run Tests (Optional)
```bash
pip install -r requirements-dev.txt
pytest tests/
```

---

## Common Tasks

### 📊 Load & Process Data
```python
from src.data import fetch_spacex_launches, load_raw_data, save_raw_data
from src.data.processing import handle_missing_values, encode_categorical

# Get data from API
launches = fetch_spacex_launches()
save_raw_data(launches, 'launches.csv')

# Or load from file
launches = load_raw_data('launches.csv')

# Clean data
launches = handle_missing_values(launches, strategy='mean')
launches = encode_categorical(launches, ['site'], method='onehot')
```

### 📈 Visualize Data
```python
from src.features import plot_distribution, plot_correlation_matrix, save_figure

# Create plots
fig1 = plot_distribution(launches, 'payload_mass_kg')
fig2 = plot_correlation_matrix(launches)

# Save to notebooks/figures/
save_figure(fig1, 'payload_dist.png')
save_figure(fig2, 'correlation.png')
```

### 🤖 Train Model
```python
from src.models import ModelTrainer

# Create trainer
trainer = ModelTrainer(model_type='random_forest')

# Split data
X_train, X_test, y_train, y_test = trainer.split_data(X, y)

# Train
trainer.train(X_train, y_train)

# Evaluate
metrics = trainer.evaluate(X_test, y_test)
print(f"Accuracy: {metrics['accuracy']:.4f}")
print(f"F1: {metrics['f1']:.4f}")

# Save model
trainer.save_model('my_model.pkl')
```

### 🔄 Cross-Validation
```python
# Run cross-validation
cv_results = trainer.cross_validate(X, y, cv=5)
print(f"CV Score: {cv_results['cv_mean']:.4f}")

# Hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15]
}
trainer.hyperparameter_tune(X_train, y_train, param_grid, cv=5)
trainer.save_model('tuned_model.pkl')
```

### 📝 Create Features
```python
from src.features.engineering import (
    create_datetime_features,
    create_interaction_features,
    select_top_features
)

# DateTime features
df = create_datetime_features(df, 'launch_date')

# Interactions
df = create_interaction_features(df, [('cost', 'mass'), ('year', 'month')])

# Feature selection
top_features = select_top_features(X, y, method='mutual_info', n_features=10)
print(f"Top features: {top_features}")
```

### 📝 Add Logging
```python
from src.logger import setup_logger

logger = setup_logger(__name__, log_file='my_script.log')

logger.info("Starting analysis")
logger.warning("No data found")
logger.error("Processing failed")
```

---

## File Locations

| Type | Location |
|------|----------|
| **Original Notebooks** | `notebooks/original/` |
| **New Analysis** | `notebooks/exploratory/` |
| **Saved Figures** | `notebooks/figures/` |
| **Raw Data** | `data/raw/` |
| **Processed Data** | `data/processed/` |
| **Models** | `models/` |
| **Logs** | `logs/` |
| **Source Code** | `src/` |
| **Tests** | `tests/` |
| **Docs** | `docs/` |

---

## Key Modules

### `src.data` - Data Operations
- `fetch_spacex_launches()` - Get data from API
- `load_raw_data()` - Load CSV
- `handle_missing_values()` - Clean data
- `remove_outliers()` - Remove outliers
- `encode_categorical()` - Encode categories
- `normalize_features()` - Scale data

### `src.features` - Visualizations & Features
- `plot_distribution()` - Plot distributions
- `plot_correlation_matrix()` - Correlation heatmap
- `plot_scatter()` - Scatter plots
- `save_figure()` - Save plots
- `create_datetime_features()` - Extract dates
- `create_interaction_features()` - Feature interactions
- `select_top_features()` - Select best features

### `src.models` - Model Training
- `ModelTrainer` class with:
  - `split_data()` - Train-test split
  - `train()` - Train model
  - `evaluate()` - Get metrics
  - `cross_validate()` - CV scores
  - `hyperparameter_tune()` - GridSearchCV
  - `predict()` - Make predictions
  - `save_model()` - Save to file
  - `load_model()` - Load from file

---

## Configuration

### Environment Variables (`.env`)
Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
```

Variables:
- `SPACEX_API_URL` - API endpoint
- `TEST_SIZE` - Test split size (0.2)
- `RANDOM_STATE` - Seed (42)
- `LOG_LEVEL` - Logging level (INFO)

---

## Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main documentation |
| `docs/API.md` | Complete API reference |
| `CONTRIBUTING.md` | Development guide |
| `REFACTORING_COMPLETE.md` | Refactoring summary |
| `PROJECT_REFACTORING.md` | Detailed changes |
| `QUICKSTART.md` | This file |

---

## Code Quality

### Format Code
```bash
pip install -r requirements-dev.txt
black src/ tests/
```

### Lint Code
```bash
flake8 src/ tests/
```

### Type Check
```bash
mypy src/
```

### Run Tests
```bash
pytest tests/ --cov=src
```

---

## Troubleshooting

### Import Errors
Make sure you're in the project directory:
```bash
cd AppliedDataScienceCapstone
```

### Missing Dependencies
Install requirements:
```bash
pip install -r requirements.txt
```

### API Errors
Check internet connection. SpaceX API may be temporarily unavailable.

### File Not Found
Check file paths are relative to project root:
```python
# ✅ Correct
data = load_raw_data('launches.csv')  # Looks in data/raw/

# ❌ Wrong
data = load_raw_data('/home/user/launches.csv')
```

---

## Common Workflows

### 1. Analyze Original Data
```bash
jupyter notebook notebooks/original/
```
Open any of the 10 notebooks to see original analysis with graphs!

### 2. New Analysis
```bash
jupyter notebook notebooks/exploratory/
```
Create new notebooks using modular code.

### 3. Model Development
```python
from src.data import fetch_spacex_launches
from src.data.processing import handle_missing_values
from src.models import ModelTrainer

# Load & clean
data = fetch_spacex_launches()
data = handle_missing_values(data)
X, y = prepare_features(data)

# Train & evaluate
trainer = ModelTrainer(model_type='random_forest')
X_train, X_test, y_train, y_test = trainer.split_data(X, y)
trainer.train(X_train, y_train)
metrics = trainer.evaluate(X_test, y_test)
print(metrics)

# Save
trainer.save_model('best_model.pkl')
```

### 4. Feature Engineering
```python
from src.features.engineering import create_datetime_features, select_top_features

data = create_datetime_features(data, 'date')
top_feats = select_top_features(X, y, n_features=10)
```

### 5. Visualization
```python
from src.features import plot_distribution, save_figure

fig = plot_distribution(data, 'payload_mass_kg')
save_figure(fig, 'payload_analysis.png')
```

---

## Useful Commands

```bash
# Install in development mode
pip install -e .

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Format code
black src/ tests/

# Check style
flake8 src/

# Type check
mypy src/

# Start Jupyter
jupyter notebook

# View git status
git status

# See what changed
git diff
```

---

## Getting Help

1. **API Reference**: `docs/API.md` - Function signatures and examples
2. **README**: `README.md` - Project overview
3. **Contributing**: `CONTRIBUTING.md` - Development guide
4. **Tests**: `tests/` - See how functions are used
5. **Original Notebooks**: `notebooks/original/` - See real examples

---

## Next Steps

1. ✅ Setup complete? Great!
2. 📊 View original notebooks in `notebooks/original/`
3. 📖 Read `README.md` for full documentation
4. 🧪 Run `pytest tests/` to verify everything works
5. 💻 Start using modular functions from `src/`
6. 📝 Create new notebooks in `notebooks/exploratory/`
7. 📈 Generate visualizations and save to `notebooks/figures/`

---

**Happy Data Science! 🎉**

For more details, see `README.md` and `docs/API.md`
