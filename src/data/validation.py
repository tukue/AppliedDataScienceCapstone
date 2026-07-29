"""Data validation utilities for modeling workflows."""

from typing import Iterable, Optional

import pandas as pd
from pandas.api.types import is_numeric_dtype


def validate_required_columns(df: pd.DataFrame, required_columns: Iterable[str]) -> None:
    """
    Validate that all required columns are present.

    Args:
        df: Input DataFrame
        required_columns: Columns that must exist

    Raises:
        ValueError: If any required column is missing
    """
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required column(s): {', '.join(missing_columns)}")


def validate_binary_target(df: pd.DataFrame, target_column: str) -> None:
    """
    Validate that a target column exists and contains only binary values.

    Args:
        df: Input DataFrame
        target_column: Target column name

    Raises:
        ValueError: If the target is missing, empty, nullable, or non-binary
    """
    validate_required_columns(df, [target_column])

    target = df[target_column]
    if target.isna().any():
        raise ValueError(f"Target column '{target_column}' contains missing values.")

    unique_values = set(target.unique())
    if not unique_values:
        raise ValueError(f"Target column '{target_column}' is empty or has no valid values.")

    valid_values = {0, 1, False, True}
    if not unique_values.issubset(valid_values):
        raise ValueError(f"Target column '{target_column}' must be binary.")


def validate_numeric_columns(df: pd.DataFrame, numeric_columns: Iterable[str]) -> None:
    """
    Validate that selected columns are numeric.

    Args:
        df: Input DataFrame
        numeric_columns: Columns expected to be numeric

    Raises:
        ValueError: If a column is missing or non-numeric
    """
    validate_required_columns(df, numeric_columns)
    non_numeric_columns = [column for column in numeric_columns if not is_numeric_dtype(df[column])]
    if non_numeric_columns:
        raise ValueError(f"Non-numeric column(s): {', '.join(non_numeric_columns)}")


def validate_non_negative(df: pd.DataFrame, columns: Iterable[str]) -> None:
    """
    Validate that selected numeric columns do not contain negative values.

    Args:
        df: Input DataFrame
        columns: Numeric columns expected to be non-negative

    Raises:
        ValueError: If negative values are present
    """
    validate_numeric_columns(df, columns)
    invalid_columns = [column for column in columns if (df[column].dropna() < 0).any()]
    if invalid_columns:
        raise ValueError(f"Negative value(s) found in: {', '.join(invalid_columns)}")


def validate_null_rates(
    df: pd.DataFrame,
    max_null_rate: float = 0.5,
    columns: Optional[Iterable[str]] = None,
) -> None:
    """
    Validate that selected columns stay below a maximum null-rate threshold.

    Args:
        df: Input DataFrame
        max_null_rate: Maximum allowed null proportion per column
        columns: Optional subset of columns to validate

    Raises:
        ValueError: If a column exceeds the configured null-rate threshold
    """
    if not 0 <= max_null_rate <= 1:
        raise ValueError("max_null_rate must be between 0 and 1.")

    selected_columns = list(columns) if columns is not None else list(df.columns)
    validate_required_columns(df, selected_columns)

    invalid_columns = [
        column for column in selected_columns if df[column].isna().mean() > max_null_rate
    ]
    if invalid_columns:
        raise ValueError(
            f"Column(s) exceed max null rate {max_null_rate}: {', '.join(invalid_columns)}"
        )


def validate_feature_target_separation(feature_columns: Iterable[str], target_column: str) -> None:
    """
    Validate that the target is not included in model features.

    Args:
        feature_columns: Model feature columns
        target_column: Target column name

    Raises:
        ValueError: If the target appears in the feature list
    """
    if target_column in set(feature_columns):
        raise ValueError(f"Target column '{target_column}' must not be used as a feature.")


def validate_modeling_data(
    df: pd.DataFrame,
    target_column: str,
    feature_columns: Optional[Iterable[str]] = None,
    required_columns: Optional[Iterable[str]] = None,
    numeric_columns: Optional[Iterable[str]] = None,
    non_negative_columns: Optional[Iterable[str]] = None,
    max_null_rate: float = 0.5,
) -> None:
    """
    Run standard validation checks before model training.

    Args:
        df: Input DataFrame
        target_column: Binary target column
        feature_columns: Optional model feature columns
        required_columns: Optional required columns
        numeric_columns: Optional numeric columns
        non_negative_columns: Optional non-negative numeric columns
        max_null_rate: Maximum allowed null proportion per validated column
    """
    if df.empty:
        raise ValueError("Modeling data must contain at least one row.")

    required = set(required_columns or [])
    required.add(target_column)
    if feature_columns is not None:
        required.update(feature_columns)
        validate_feature_target_separation(feature_columns, target_column)

    validate_required_columns(df, required)
    validate_binary_target(df, target_column)
    validate_null_rates(df, max_null_rate=max_null_rate, columns=required)

    if numeric_columns is not None:
        validate_numeric_columns(df, numeric_columns)

    if non_negative_columns is not None:
        validate_non_negative(df, non_negative_columns)
