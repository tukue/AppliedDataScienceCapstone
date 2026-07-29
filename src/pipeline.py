"""Runnable training pipeline for reproducible local model artifacts."""

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple

import pandas as pd

from src.config import PROCESSED_DATA_DIR, RANDOM_STATE, REPORTS_DIR, TEST_SIZE
from src.data.processing import encode_categorical, handle_missing_values
from src.data.validation import validate_modeling_data
from src.features.engineering import create_datetime_features
from src.models import ModelTrainer

TARGET_COLUMN = "landing_success"
MODEL_TYPE = "random_forest"


def build_sample_launch_data() -> pd.DataFrame:
    """
    Build deterministic sample launch data for CI-safe pipeline execution.

    Returns:
        Sample launch DataFrame with source-style columns
    """
    data = {
        "flight_number": list(range(1, 25)),
        "payload_mass_kg": [
            350,
            525,
            677,
            500,
            3170,
            3325,
            2296,
            1316,
            4535,
            4428,
            2216,
            2395,
            570,
            4150,
            5600,
            5300,
            9600,
            2490,
            6070,
            2708,
            9600,
            12259,
            15600,
            13200,
        ],
        "orbit": [
            "LEO",
            "LEO",
            "ISS",
            "PO",
            "GTO",
            "GTO",
            "ISS",
            "LEO",
            "GTO",
            "GTO",
            "ISS",
            "LEO",
            "PO",
            "GTO",
            "ISS",
            "LEO",
            "GTO",
            "ISS",
            "GTO",
            "PO",
            "LEO",
            "GTO",
            "ISS",
            "GTO",
        ],
        "launch_site": [
            "CCAFS SLC 40",
            "CCAFS SLC 40",
            "KSC LC 39A",
            "VAFB SLC 4E",
            "CCAFS SLC 40",
            "CCAFS SLC 40",
            "KSC LC 39A",
            "CCAFS SLC 40",
            "KSC LC 39A",
            "CCAFS SLC 40",
            "KSC LC 39A",
            "VAFB SLC 4E",
            "VAFB SLC 4E",
            "CCAFS SLC 40",
            "KSC LC 39A",
            "KSC LC 39A",
            "CCAFS SLC 40",
            "KSC LC 39A",
            "CCAFS SLC 40",
            "VAFB SLC 4E",
            "KSC LC 39A",
            "CCAFS SLC 40",
            "KSC LC 39A",
            "CCAFS SLC 40",
        ],
        "reused": [
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
        ],
        "launch_date": pd.date_range("2014-01-01", periods=24, freq="90D").astype(str),
        TARGET_COLUMN: [
            0,
            0,
            1,
            0,
            0,
            1,
            1,
            1,
            0,
            0,
            1,
            0,
            1,
            1,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            0,
            1,
            1,
        ],
    }
    validate_equal_lengths(data, context="sample launch data")
    return pd.DataFrame(data)


def validate_equal_lengths(data: Mapping[str, Iterable], context: str) -> None:
    """
    Validate that tabular source arrays can be combined safely.

    Args:
        data: Mapping of column names to column values
        context: Human-readable data source name

    Raises:
        ValueError: If columns have inconsistent lengths
    """
    lengths = {column: len(values) for column, values in data.items()}
    if len(set(lengths.values())) != 1:
        raise ValueError(f"Array length mismatch in {context}: {lengths}")


def prepare_modeling_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Validate and prepare source-style launch data for model training.

    Args:
        df: Source-style launch DataFrame

    Returns:
        Feature matrix, target series, and processed DataFrame
    """
    required_columns = [
        "flight_number",
        "payload_mass_kg",
        "orbit",
        "launch_site",
        "reused",
        "launch_date",
        TARGET_COLUMN,
    ]
    validate_modeling_data(
        df,
        target_column=TARGET_COLUMN,
        required_columns=required_columns,
        numeric_columns=["flight_number", "payload_mass_kg"],
        non_negative_columns=["payload_mass_kg"],
        max_null_rate=0.25,
    )

    processed = handle_missing_values(df, strategy="median")
    processed = create_datetime_features(processed, "launch_date")
    processed["reused"] = processed["reused"].astype(int)
    processed = encode_categorical(processed, ["orbit", "launch_site"], method="onehot")
    processed = processed.drop(columns=["launch_date"])

    feature_columns = [column for column in processed.columns if column != TARGET_COLUMN]
    validate_modeling_data(
        processed,
        target_column=TARGET_COLUMN,
        feature_columns=feature_columns,
        numeric_columns=feature_columns,
        non_negative_columns=["payload_mass_kg"],
        max_null_rate=0,
    )

    return processed[feature_columns], processed[TARGET_COLUMN], processed


def train_pipeline(df: pd.DataFrame = None) -> Dict[str, float]:
    """
    Run the full sample-data training pipeline and persist reports.

    Args:
        df: Optional source-style launch DataFrame

    Returns:
        Evaluation metrics
    """
    source_data = build_sample_launch_data() if df is None else df
    X, y, processed = prepare_modeling_data(source_data)

    trainer = ModelTrainer(model_type=MODEL_TYPE, random_state=RANDOM_STATE)
    X_train, X_test, y_train, y_test = trainer.split_data(X, y, test_size=TEST_SIZE)
    trainer.train(X_train, y_train)
    metrics = trainer.evaluate(X_test, y_test)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    processed.to_csv(PROCESSED_DATA_DIR / "sample_modeling_data.csv", index=False)
    trainer.save_model("sample_random_forest.joblib")
    write_json(REPORTS_DIR / "metrics.json", metrics)
    write_json(
        REPORTS_DIR / "model_config.json",
        {
            "model_type": MODEL_TYPE,
            "target_column": TARGET_COLUMN,
            "feature_columns": list(X.columns),
            "test_size": TEST_SIZE,
            "random_state": RANDOM_STATE,
            "input_rows": len(source_data),
        },
    )

    return metrics


def write_json(path: Path, payload: Dict) -> None:
    """
    Write a JSON artifact with stable formatting.

    Args:
        path: Output path
        payload: JSON-serializable content
    """
    serializable_payload = to_json_serializable(payload)
    path.write_text(json.dumps(serializable_payload, indent=2, sort_keys=True))


def to_json_serializable(value: Any) -> Any:
    """
    Convert common data-science objects into JSON-serializable values.

    Args:
        value: Value to convert

    Returns:
        JSON-compatible value
    """
    if isinstance(value, dict):
        return {key: to_json_serializable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_json_serializable(item) for item in value]
    if hasattr(value, "tolist"):
        return to_json_serializable(value.tolist())
    if hasattr(value, "item"):
        try:
            return value.item()
        except (AttributeError, TypeError, ValueError):
            return str(value)

    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return str(value)


def main() -> None:
    """Run the pipeline from the command line."""
    metrics = train_pipeline()
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
