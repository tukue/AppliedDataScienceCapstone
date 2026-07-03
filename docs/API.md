# API Documentation

## Data Module

### `src.data` - Data Loading and Collection

#### Functions

##### `fetch_spacex_launches(endpoint: str = "/launches") -> pd.DataFrame`
Fetch SpaceX launch data from official API.

**Parameters:**
- `endpoint` (str): API endpoint to fetch from. Default: "/launches"

**Returns:**
- `pd.DataFrame`: DataFrame with launch data

**Example:**
```python
from src.data import fetch_spacex_launches

launches = fetch_spacex_launches()
rockets = fetch_spacex_launches("/rockets")
```

---

##### `fetch_spacex_rockets(endpoint: str = "/rockets") -> pd.DataFrame`
Fetch SpaceX rocket information.

**Parameters:**
- `endpoint` (str): API endpoint. Default: "/rockets"

**Returns:**
- `pd.DataFrame`: DataFrame with rocket data

---

##### `fetch_spacex_cores(endpoint: str = "/cores") -> pd.DataFrame`
Fetch SpaceX core/booster information.

**Parameters:**
- `endpoint` (str): API endpoint. Default: "/cores"

**Returns:**
- `pd.DataFrame`: DataFrame with core data

---

##### `save_raw_data(df: pd.DataFrame, filename: str) -> None`
Save raw data to CSV file in `data/raw/` directory.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to save
- `filename` (str): Output filename

**Example:**
```python
from src.data import fetch_spacex_launches, save_raw_data

launches = fetch_spacex_launches()
save_raw_data(launches, 'spacex_launches.csv')
```

---

##### `load_raw_data(filename: str) -> pd.DataFrame`
Load raw data from CSV file.

**Parameters:**
- `filename` (str): Input filename in `data/raw/` directory

**Returns:**
- `pd.DataFrame`: Loaded DataFrame

---

## Data Processing Module

### `src.data.processing` - Data Cleaning and Transformation

#### Functions

##### `handle_missing_values(df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame`
Handle missing values in the dataset.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `strategy` (str): Strategy to use - 'drop', 'mean', 'median', or 'forward_fill'

**Returns:**
- `pd.DataFrame`: DataFrame with missing values handled

**Example:**
```python
from src.data.processing import handle_missing_values

df = handle_missing_values(df, strategy='mean')
```

---

##### `remove_outliers(df: pd.DataFrame, column: str, threshold: float = 1.5) -> pd.DataFrame`
Remove outliers using IQR method.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `column` (str): Column name to check for outliers
- `threshold` (float): IQR multiplier. Default: 1.5

**Returns:**
- `pd.DataFrame`: DataFrame with outliers removed

---

##### `encode_categorical(df: pd.DataFrame, columns: List[str], method: str = "onehot") -> pd.DataFrame`
Encode categorical variables.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `columns` (List[str]): Categorical column names
- `method` (str): 'onehot' or 'label'

**Returns:**
- `pd.DataFrame`: DataFrame with encoded features

---

##### `normalize_features(df: pd.DataFrame, columns: List[str], method: str = "standard") -> pd.DataFrame`
Normalize numeric features.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `columns` (List[str]): Numeric column names
- `method` (str): 'standard' or 'minmax'

**Returns:**
- `pd.DataFrame`: DataFrame with normalized features

---

## Features Module

### `src.features` - Visualization Utilities

#### Functions

##### `save_figure(fig: plt.Figure, filename: str, dpi: int = 300) -> Path`
Save figure to `notebooks/figures/` directory.

**Parameters:**
- `fig` (plt.Figure): Matplotlib figure object
- `filename` (str): Output filename
- `dpi` (int): Resolution. Default: 300

**Returns:**
- `Path`: Path to saved figure

---

##### `plot_distribution(df: pd.DataFrame, column: str, title: str = None) -> plt.Figure`
Plot distribution of a column.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `column` (str): Column to plot
- `title` (str): Plot title (optional)

**Returns:**
- `plt.Figure`: Matplotlib figure

---

##### `plot_correlation_matrix(df: pd.DataFrame, figsize: Tuple = (12, 10)) -> plt.Figure`
Plot correlation matrix heatmap.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `figsize` (Tuple): Figure size

**Returns:**
- `plt.Figure`: Matplotlib figure with correlation heatmap

---

##### `plot_scatter(df: pd.DataFrame, x: str, y: str, title: str = None) -> plt.Figure`
Plot scatter plot.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `x` (str): X-axis column
- `y` (str): Y-axis column
- `title` (str): Plot title (optional)

**Returns:**
- `plt.Figure`: Matplotlib figure

---

### `src.features.engineering` - Feature Engineering

#### Functions

##### `create_datetime_features(df: pd.DataFrame, date_column: str) -> pd.DataFrame`
Extract datetime features from a date column.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `date_column` (str): Date column name

**Returns:**
- `pd.DataFrame`: DataFrame with new datetime features (year, month, day, etc.)

---

##### `create_interaction_features(df: pd.DataFrame, feature_pairs: List[Tuple]) -> pd.DataFrame`
Create interaction features from feature pairs.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `feature_pairs` (List[Tuple]): List of (col1, col2) tuples

**Returns:**
- `pd.DataFrame`: DataFrame with interaction features

---

##### `create_polynomial_features(df: pd.DataFrame, columns: List[str], degree: int = 2) -> pd.DataFrame`
Create polynomial features.

**Parameters:**
- `df` (pd.DataFrame): Input DataFrame
- `columns` (List[str]): Column names to create polynomials from
- `degree` (int): Polynomial degree. Default: 2

**Returns:**
- `pd.DataFrame`: DataFrame with polynomial features

---

##### `select_top_features(X: pd.DataFrame, y: pd.Series, method: str = "mutual_info", n_features: int = 10) -> List[str]`
Select top N features using specified method.

**Parameters:**
- `X` (pd.DataFrame): Feature DataFrame
- `y` (pd.Series): Target series
- `method` (str): 'mutual_info', 'correlation', or 'variance'
- `n_features` (int): Number of features to select. Default: 10

**Returns:**
- `List[str]`: List of top feature names

---

## Models Module

### `src.models.ModelTrainer` - Model Training and Evaluation

#### Class: `ModelTrainer`

##### Initialization
```python
from src.models import ModelTrainer

trainer = ModelTrainer(model_type='random_forest', random_state=42)
```

**Parameters:**
- `model_type` (str): Type of model - 'random_forest' (default), 'gradient_boost', 'logistic', 'svm'
- `random_state` (int): Random state for reproducibility

##### Methods

###### `split_data(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Tuple`
Split data into train and test sets.

**Returns:**
- `Tuple`: (X_train, X_test, y_train, y_test)

---

###### `train(X_train: pd.DataFrame, y_train: pd.Series) -> None`
Train the model.

---

###### `evaluate(X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]`
Evaluate model on test set.

**Returns:**
- `Dict`: Dictionary with metrics (accuracy, precision, recall, f1, roc_auc)

---

###### `cross_validate(X: pd.DataFrame, y: pd.Series, cv: int = 5) -> Dict[str, float]`
Perform cross-validation.

**Returns:**
- `Dict`: Dictionary with cv_mean, cv_std, cv_scores

---

###### `hyperparameter_tune(X_train: pd.DataFrame, y_train: pd.Series, param_grid: Dict, cv: int = 5) -> None`
Perform hyperparameter tuning using GridSearchCV.

---

###### `save_model(filename: str) -> Path`
Save trained model to file.

**Returns:**
- `Path`: Path to saved model

---

###### `load_model(filename: str) -> None`
Load trained model from file.

---

###### `predict(X: pd.DataFrame) -> np.ndarray`
Make predictions.

**Returns:**
- `np.ndarray`: Predictions

---

###### `predict_proba(X: pd.DataFrame) -> np.ndarray`
Make probability predictions.

**Returns:**
- `np.ndarray`: Probability predictions

---

## Configuration

### `src.config` - Project Configuration

**Key Variables:**
- `PROJECT_ROOT`: Root directory of the project
- `DATA_DIR`: Data directory
- `RAW_DATA_DIR`: Raw data directory
- `PROCESSED_DATA_DIR`: Processed data directory
- `MODELS_DIR`: Models directory
- `LOGS_DIR`: Logs directory
- `SPACEX_API_URL`: SpaceX API base URL
- `TEST_SIZE`: Default test set size (0.2)
- `RANDOM_STATE`: Default random state (42)
- `CV_FOLDS`: Default cross-validation folds (5)

---

## Logging

### `src.logger` - Logging Setup

#### Function

##### `setup_logger(name: str, log_file: str = None) -> logging.Logger`
Set up a logger with console and optional file handlers.

**Parameters:**
- `name` (str): Logger name (typically `__name__`)
- `log_file` (str): Optional log file path

**Returns:**
- `logging.Logger`: Configured logger instance

**Example:**
```python
from src.logger import setup_logger

logger = setup_logger(__name__, log_file='my_script.log')
logger.info("Starting analysis...")
```

---

## Complete Workflow Example

```python
from src.data import fetch_spacex_launches, save_raw_data
from src.data.processing import handle_missing_values, encode_categorical
from src.features import plot_distribution, save_figure
from src.features.engineering import create_datetime_features
from src.models import ModelTrainer
from src.logger import setup_logger

logger = setup_logger(__name__)

# 1. Data Collection
logger.info("Fetching SpaceX launch data...")
launches = fetch_spacex_launches()
save_raw_data(launches, 'spacex_launches.csv')

# 2. Data Wrangling
logger.info("Processing data...")
launches = handle_missing_values(launches, strategy='mean')
launches = encode_categorical(launches, ['site'], method='onehot')

# 3. Feature Engineering
logger.info("Creating features...")
launches = create_datetime_features(launches, 'date_utc')

# 4. Visualization
logger.info("Visualizing data...")
fig = plot_distribution(launches, 'payload_mass_kg')
save_figure(fig, 'payload_distribution.png')

# 5. Model Training
logger.info("Training model...")
trainer = ModelTrainer(model_type='random_forest')
X_train, X_test, y_train, y_test = trainer.split_data(X, y)
trainer.train(X_train, y_train)
metrics = trainer.evaluate(X_test, y_test)
print(f"Accuracy: {metrics['accuracy']:.4f}")

# 6. Model Persistence
trainer.save_model('spacex_landing_predictor.pkl')
logger.info("Workflow completed successfully!")
```
