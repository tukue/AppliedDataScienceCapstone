"""Feature engineering utilities."""

import pandas as pd
import numpy as np
from typing import List, Tuple
from src.logger import setup_logger

logger = setup_logger(__name__)


def create_datetime_features(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Extract datetime features from a date column.

    Args:
        df: Input DataFrame
        date_column: Date column name

    Returns:
        DataFrame with new datetime features
    """
    df[date_column] = pd.to_datetime(df[date_column])

    df[f"{date_column}_year"] = df[date_column].dt.year
    df[f"{date_column}_month"] = df[date_column].dt.month
    df[f"{date_column}_day"] = df[date_column].dt.day
    df[f"{date_column}_dayofweek"] = df[date_column].dt.dayofweek
    df[f"{date_column}_quarter"] = df[date_column].dt.quarter

    logger.info(f"Created datetime features from {date_column}")
    return df


def create_interaction_features(df: pd.DataFrame, feature_pairs: List[Tuple]) -> pd.DataFrame:
    """
    Create interaction features from feature pairs.

    Args:
        df: Input DataFrame
        feature_pairs: List of (col1, col2) tuples

    Returns:
        DataFrame with interaction features
    """
    for col1, col2 in feature_pairs:
        if col1 in df.columns and col2 in df.columns:
            df[f"{col1}_x_{col2}"] = df[col1] * df[col2]
            logger.info(f"Created interaction feature: {col1}_x_{col2}")

    return df


def create_polynomial_features(
    df: pd.DataFrame, columns: List[str], degree: int = 2
) -> pd.DataFrame:
    """
    Create polynomial features.

    Args:
        df: Input DataFrame
        columns: Column names to create polynomials from
        degree: Polynomial degree

    Returns:
        DataFrame with polynomial features
    """
    from sklearn.preprocessing import PolynomialFeatures

    poly = PolynomialFeatures(degree=degree, include_bias=False)
    poly_features = poly.fit_transform(df[columns])

    feature_names = poly.get_feature_names_out(columns)
    poly_df = pd.DataFrame(poly_features, columns=feature_names)

    df = pd.concat([df, poly_df], axis=1)
    logger.info(f"Created {len(feature_names)} polynomial features")

    return df


def select_top_features(
    X: pd.DataFrame, y: pd.Series, method: str = "mutual_info", n_features: int = 10
) -> List[str]:
    """
    Select top N features using specified method.

    Args:
        X: Feature DataFrame
        y: Target series
        method: 'mutual_info', 'correlation', or 'variance'
        n_features: Number of features to select

    Returns:
        List of top feature names
    """
    if method == "mutual_info":
        from sklearn.feature_selection import mutual_info_classif

        scores = mutual_info_classif(X, y)
        feature_names = X.columns[np.argsort(scores)[-n_features:]]

    elif method == "correlation":
        correlations = X.corrwith(y).abs().sort_values(ascending=False)
        feature_names = correlations[:n_features].index.tolist()

    elif method == "variance":
        variances = X.var().sort_values(ascending=False)
        feature_names = variances[:n_features].index.tolist()

    logger.info(f"Selected {n_features} features using {method}")
    return feature_names.tolist() if hasattr(feature_names, "tolist") else list(feature_names)
