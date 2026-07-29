"""Unit tests for data validation utilities."""

import pandas as pd
import pytest

from src.data.validation import (
    validate_binary_target,
    validate_feature_target_separation,
    validate_modeling_data,
    validate_non_negative,
    validate_null_rates,
    validate_numeric_columns,
    validate_required_columns,
)


class TestDataValidation:
    """Tests for modeling data validation."""

    def test_validate_required_columns_passes(self):
        """Test required-column validation with valid data."""
        df = pd.DataFrame({"payload_mass_kg": [1000], "landing_success": [1]})

        validate_required_columns(df, ["payload_mass_kg", "landing_success"])

    def test_validate_required_columns_raises_for_missing_column(self):
        """Test required-column validation failure."""
        df = pd.DataFrame({"payload_mass_kg": [1000]})

        with pytest.raises(ValueError, match="Missing required column"):
            validate_required_columns(df, ["landing_success"])

    def test_validate_binary_target_passes(self):
        """Test binary-target validation with 0/1 values."""
        df = pd.DataFrame({"landing_success": [0, 1, 1]})

        validate_binary_target(df, "landing_success")

    def test_validate_binary_target_raises_for_non_binary_values(self):
        """Test binary-target validation rejects multiclass values."""
        df = pd.DataFrame({"landing_success": [0, 1, 2]})

        with pytest.raises(ValueError, match="must be binary"):
            validate_binary_target(df, "landing_success")

    def test_validate_binary_target_raises_for_empty_target(self):
        """Test binary-target validation rejects empty standalone target data."""
        df = pd.DataFrame({"landing_success": []})

        with pytest.raises(ValueError, match="empty or has no valid values"):
            validate_binary_target(df, "landing_success")

    def test_validate_numeric_columns_raises_for_non_numeric_column(self):
        """Test numeric-column validation rejects strings."""
        df = pd.DataFrame({"payload_mass_kg": ["heavy"]})

        with pytest.raises(ValueError, match="Non-numeric"):
            validate_numeric_columns(df, ["payload_mass_kg"])

    def test_validate_non_negative_raises_for_negative_values(self):
        """Test non-negative validation rejects negative payload mass."""
        df = pd.DataFrame({"payload_mass_kg": [1000, -1]})

        with pytest.raises(ValueError, match="Negative value"):
            validate_non_negative(df, ["payload_mass_kg"])

    def test_validate_null_rates_raises_when_threshold_exceeded(self):
        """Test null-rate validation failure."""
        df = pd.DataFrame({"payload_mass_kg": [1000, None, None]})

        with pytest.raises(ValueError, match="exceed max null rate"):
            validate_null_rates(df, max_null_rate=0.5)

    def test_validate_feature_target_separation_raises_for_target_leakage(self):
        """Test feature-target validation catches leakage."""
        with pytest.raises(ValueError, match="must not be used as a feature"):
            validate_feature_target_separation(
                ["payload_mass_kg", "landing_success"], "landing_success"
            )

    def test_validate_modeling_data_passes_valid_data(self):
        """Test full modeling validation with valid data."""
        df = pd.DataFrame(
            {
                "payload_mass_kg": [1000, 2000],
                "flight_number": [1, 2],
                "landing_success": [0, 1],
            }
        )

        validate_modeling_data(
            df,
            target_column="landing_success",
            feature_columns=["payload_mass_kg", "flight_number"],
            numeric_columns=["payload_mass_kg", "flight_number"],
            non_negative_columns=["payload_mass_kg"],
            max_null_rate=0,
        )

    def test_validate_modeling_data_raises_for_empty_data(self):
        """Test full modeling validation rejects empty data."""
        df = pd.DataFrame(columns=["payload_mass_kg", "landing_success"])

        with pytest.raises(ValueError, match="at least one row"):
            validate_modeling_data(df, target_column="landing_success")
