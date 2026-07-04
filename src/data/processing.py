"""Data processing and wrangling utilities."""

import pandas as pd
import numpy as np
from typing import List
from src.logger import setup_logger

logger = setup_logger(__name__)


def handle_missing_values(df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
    """
    Handle missing values in the dataset.

    Args:
        df: Input DataFrame
        strategy: 'drop', 'mean', 'median', or 'forward_fill'

    Returns:
        DataFrame with missing values handled
    """
    logger.info(f"Handling missing values with strategy: {strategy}")

    if strategy == "drop":
        df = df.dropna()
    elif strategy == "mean":
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == "median":
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif strategy == "forward_fill":
        df = df.fillna(method="ffill")

    logger.info(f"Missing values after handling: {df.isnull().sum().sum()}")
    return df


def remove_outliers(df: pd.DataFrame, column: str, threshold: float = 1.5) -> pd.DataFrame:
    """
    Remove outliers using IQR method.

    Args:
        df: Input DataFrame
        column: Column name to check for outliers
        threshold: IQR multiplier (default 1.5)

    Returns:
        DataFrame with outliers removed
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR

    before = len(df)
    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    after = len(df)

    logger.info(f"Removed {before - after} outliers from {column}")
    return df


def encode_categorical(
    df: pd.DataFrame, columns: List[str], method: str = "onehot"
) -> pd.DataFrame:
    """
    Encode categorical variables.

    Args:
        df: Input DataFrame
        columns: Categorical column names
        method: 'onehot' or 'label'

    Returns:
        DataFrame with encoded features
    """
    logger.info(f"Encoding {len(columns)} categorical features using {method}")

    if method == "onehot":
        df = pd.get_dummies(df, columns=columns, drop_first=True)
    elif method == "label":
        from sklearn.preprocessing import LabelEncoder

        for col in columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))

    return df


def normalize_features(
    df: pd.DataFrame, columns: List[str], method: str = "standard"
) -> pd.DataFrame:
    """
    Normalize numeric features.

    Args:
        df: Input DataFrame
        columns: Numeric column names
        method: 'standard' or 'minmax'

    Returns:
        DataFrame with normalized features
    """
    logger.info(f"Normalizing {len(columns)} features using {method} scaling")

    from sklearn.preprocessing import StandardScaler, MinMaxScaler

    scaler = StandardScaler() if method == "standard" else MinMaxScaler()
    df = df.copy()
    df.loc[:, columns] = scaler.fit_transform(df[columns])

    return df
