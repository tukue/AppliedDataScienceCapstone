"""Unit tests for the runnable pipeline."""

import json

import numpy as np
import pandas as pd
import pytest

from src.pipeline import (
    build_sample_launch_data,
    prepare_modeling_data,
    to_json_serializable,
    train_pipeline,
    validate_equal_lengths,
    write_json,
)


class TestPipeline:
    """Tests for pipeline orchestration."""

    def test_build_sample_launch_data_contains_required_columns(self):
        """Test sample data shape and required columns."""
        df = build_sample_launch_data()

        assert len(df) >= 20
        assert {
            "flight_number",
            "payload_mass_kg",
            "orbit",
            "launch_site",
            "reused",
            "launch_date",
            "landing_success",
        }.issubset(df.columns)

    def test_validate_equal_lengths_raises_for_mismatched_columns(self):
        """Test source-array validation catches inconsistent sample data."""
        data = {"flight_number": [1, 2], "payload_mass_kg": [1000]}

        with pytest.raises(ValueError, match="Array length mismatch"):
            validate_equal_lengths(data, context="test data")

    def test_prepare_modeling_data_returns_numeric_features(self):
        """Test processing creates model-ready features."""
        df = build_sample_launch_data()

        X, y, processed = prepare_modeling_data(df)

        assert "landing_success" not in X.columns
        assert len(X) == len(y) == len(processed)
        assert all(pd.api.types.is_numeric_dtype(X[column]) for column in X.columns)
        assert "launch_date" not in processed.columns

    def test_train_pipeline_writes_artifacts(self, tmp_path, monkeypatch):
        """Test pipeline writes metrics, config, processed data, and model artifacts."""
        import src.models as models_module
        import src.pipeline as pipeline_module

        monkeypatch.setattr(pipeline_module, "PROCESSED_DATA_DIR", tmp_path / "processed")
        monkeypatch.setattr(pipeline_module, "REPORTS_DIR", tmp_path / "reports")
        monkeypatch.setattr(models_module, "MODELS_DIR", tmp_path / "models")

        metrics = train_pipeline()
        metrics_path = tmp_path / "reports" / "metrics.json"
        config_path = tmp_path / "reports" / "model_config.json"

        assert {"accuracy", "precision", "recall", "f1", "roc_auc"}.issubset(metrics)
        assert (tmp_path / "processed" / "sample_modeling_data.csv").exists()
        assert (tmp_path / "models" / "sample_random_forest.joblib").exists()
        assert metrics_path.exists()
        assert config_path.exists()
        assert json.loads(metrics_path.read_text())["accuracy"] == metrics["accuracy"]

    def test_write_json_serializes_data_science_types(self, tmp_path):
        """Test JSON artifacts handle NumPy and pandas values."""
        output_path = tmp_path / "payload.json"
        payload = {
            "scalar": np.float64(0.75),
            "array": np.array([1, 2, 3]),
            "series": pd.Series([0.1, 0.2]),
            "unserializable": tmp_path,
        }

        write_json(output_path, payload)

        content = json.loads(output_path.read_text())
        assert content["scalar"] == 0.75
        assert content["array"] == [1, 2, 3]
        assert content["series"] == [0.1, 0.2]
        assert content["unserializable"] == str(tmp_path)

    def test_to_json_serializable_handles_nested_values(self):
        """Test nested payloads are converted recursively."""
        payload = {"metrics": {"fold_scores": np.array([0.6, 0.7])}}

        assert to_json_serializable(payload) == {"metrics": {"fold_scores": [0.6, 0.7]}}
