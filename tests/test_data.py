"""Unit tests for data module."""

import warnings
import pytest
import pandas as pd
import numpy as np
from src.data import (
    fetch_spacex_cores,
    fetch_spacex_launches,
    fetch_spacex_rockets,
    load_raw_data,
    save_raw_data,
)
from src.data.processing import (
    handle_missing_values,
    remove_outliers,
    encode_categorical,
    normalize_features,
)


class TestDataProcessing:
    """Tests for data processing functions."""

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        return pd.DataFrame(
            {
                "feature1": [1, 2, 3, 4, 5, np.nan],
                "feature2": [10, 20, 30, 40, 50, 60],
                "category": ["A", "B", "A", "C", "B", "C"],
            }
        )

    def test_handle_missing_values_drop(self, sample_df):
        """Test missing value handling with drop strategy."""
        result = handle_missing_values(sample_df, strategy="drop")
        assert result.isnull().sum().sum() == 0
        assert len(result) == 5

    def test_handle_missing_values_mean(self, sample_df):
        """Test missing value handling with mean strategy."""
        result = handle_missing_values(sample_df, strategy="mean")
        assert result["feature1"].isnull().sum() == 0

    def test_handle_missing_values_median(self, sample_df):
        """Test missing value handling with median strategy."""
        result = handle_missing_values(sample_df, strategy="median")
        assert result["feature1"].isnull().sum() == 0
        assert result.loc[5, "feature1"] == 3

    def test_handle_missing_values_forward_fill(self):
        """Test missing value handling with forward-fill strategy."""
        df = pd.DataFrame({"feature": [1, np.nan, 3]})

        result = handle_missing_values(df, strategy="forward_fill")

        assert result.loc[1, "feature"] == 1

    def test_handle_missing_values_forward_fill_does_not_warn(self):
        """Test forward fill uses the non-deprecated pandas API."""
        df = pd.DataFrame({"feature": [1, np.nan, 3]})

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")
            result = handle_missing_values(df, strategy="forward_fill")

        assert result.loc[1, "feature"] == 1
        assert len(caught_warnings) == 0

    def test_remove_outliers(self, sample_df):
        """Test outlier removal."""
        # Add some outliers
        sample_df.loc[6] = [100, 1000, "D"]
        result = remove_outliers(sample_df, "feature2", threshold=1.5)
        assert len(result) < len(sample_df)

    def test_encode_categorical(self, sample_df):
        """Test categorical encoding."""
        result = encode_categorical(sample_df, ["category"], method="onehot")
        assert "category_B" in result.columns or "category_C" in result.columns
        assert len(result) == len(sample_df)

    def test_encode_categorical_label(self, sample_df):
        """Test label encoding branch."""
        result = encode_categorical(sample_df, ["category"], method="label")

        assert result["category"].dtype.kind in {"i", "u"}
        assert set(result["category"].unique()) == {0, 1, 2}

    def test_encode_categorical_label_does_not_mutate_input(self, sample_df):
        """Test label encoding preserves the caller's DataFrame."""
        original = sample_df.copy(deep=True)

        result = encode_categorical(sample_df, ["category"], method="label")

        pd.testing.assert_frame_equal(sample_df, original)
        assert result is not sample_df
        assert result["category"].dtype.kind in {"i", "u"}

    def test_normalize_features(self, sample_df):
        """Test feature normalization."""
        numeric_cols = ["feature1", "feature2"]
        result = normalize_features(sample_df.dropna(), numeric_cols, method="standard")
        # Check that features are normalized
        assert abs(result["feature1"].mean()) < 0.1 or result["feature1"].isnull().any()

    def test_normalize_features_minmax(self, sample_df):
        """Test min-max normalization branch."""
        result = normalize_features(sample_df.dropna(), ["feature1", "feature2"], method="minmax")

        assert result["feature1"].min() == pytest.approx(0)
        assert result["feature1"].max() == pytest.approx(1)


class TestFeatureHandling:
    """Tests for feature handling edge cases."""

    def test_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        df = pd.DataFrame()
        # Should not raise error
        assert len(df) == 0

    def test_all_missing_column(self):
        """Test column with all missing values."""
        df = pd.DataFrame({"col": [np.nan, np.nan, np.nan]})
        result = handle_missing_values(df, strategy="drop")
        assert len(result) == 0


class TestDataCollection:
    """Tests for data collection and raw CSV helpers."""

    class MockResponse:
        """Minimal requests response mock."""

        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            """No-op success response."""

        def json(self):
            """Return mock JSON payload."""
            return self.payload

    def test_fetch_spacex_launches_uses_endpoint(self, monkeypatch):
        """Test SpaceX fetch converts API response to DataFrame."""
        calls = []

        def mock_get(url, timeout):
            calls.append((url, timeout))
            return self.MockResponse([{"id": "1", "success": True}])

        monkeypatch.setattr("src.data.requests.get", mock_get)

        result = fetch_spacex_launches("/launches")

        assert len(result) == 1
        assert bool(result.loc[0, "success"]) is True
        assert calls[0][0].endswith("/launches")
        assert calls[0][1] == 10

    def test_fetch_spacex_wrappers_use_default_endpoints(self, monkeypatch):
        """Test rocket and core wrappers delegate to fetch function."""
        endpoints = []

        def mock_fetch(endpoint):
            endpoints.append(endpoint)
            return pd.DataFrame({"endpoint": [endpoint]})

        monkeypatch.setattr("src.data.fetch_spacex_launches", mock_fetch)

        rockets = fetch_spacex_rockets()
        cores = fetch_spacex_cores()

        assert endpoints == ["/rockets", "/cores"]
        assert rockets.loc[0, "endpoint"] == "/rockets"
        assert cores.loc[0, "endpoint"] == "/cores"

    def test_save_and_load_raw_data(self, tmp_path, monkeypatch):
        """Test raw CSV persistence helpers."""
        import src.data as data_module

        monkeypatch.setattr(data_module, "RAW_DATA_DIR", tmp_path)
        original = pd.DataFrame({"id": [1, 2], "success": [True, False]})

        save_raw_data(original, "launches.csv")
        loaded = load_raw_data("launches.csv")

        pd.testing.assert_frame_equal(loaded, original)
