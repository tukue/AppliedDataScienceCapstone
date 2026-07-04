"""Unit tests for feature engineering utilities."""

import pandas as pd

from src.features.engineering import (
    create_datetime_features,
    create_interaction_features,
    create_polynomial_features,
    select_top_features,
)


class TestFeatureEngineering:
    """Tests for feature engineering helpers."""

    def test_create_datetime_features(self):
        """Test date feature extraction."""
        df = pd.DataFrame({"launch_date": ["2020-05-30"]})
        original = df.copy(deep=True)

        result = create_datetime_features(df, "launch_date")

        pd.testing.assert_frame_equal(df, original)
        assert result is not df
        assert result.loc[0, "launch_date_year"] == 2020
        assert result.loc[0, "launch_date_month"] == 5
        assert result.loc[0, "launch_date_day"] == 30
        assert result.loc[0, "launch_date_quarter"] == 2

    def test_create_interaction_features(self):
        """Test interaction feature creation skips missing pairs."""
        df = pd.DataFrame({"payload": [2, 3], "flight": [10, 20]})
        original = df.copy(deep=True)

        result = create_interaction_features(df, [("payload", "flight"), ("payload", "missing")])

        pd.testing.assert_frame_equal(df, original)
        assert result is not df
        assert "payload_x_flight" in result.columns
        assert "payload_x_missing" not in result.columns
        assert result["payload_x_flight"].tolist() == [20, 60]

    def test_create_polynomial_features(self):
        """Test polynomial feature creation."""
        df = pd.DataFrame({"payload": [2, 3], "flight": [10, 20]})

        result = create_polynomial_features(df, ["payload", "flight"], degree=2)

        assert "payload^2" in result.columns
        assert "payload flight" in result.columns
        assert result.loc[0, "payload^2"] == 4

    def test_select_top_features_correlation(self):
        """Test correlation-based feature selection."""
        X = pd.DataFrame(
            {
                "strong": [0, 1, 2, 3],
                "weak": [1, 1, 1, 2],
                "inverse": [3, 2, 1, 0],
            }
        )
        y = pd.Series([0, 1, 2, 3])

        result = select_top_features(X, y, method="correlation", n_features=2)

        assert result == ["strong", "inverse"]

    def test_select_top_features_variance(self):
        """Test variance-based feature selection."""
        X = pd.DataFrame({"low": [1, 1, 1], "high": [1, 10, 20]})
        y = pd.Series([0, 1, 1])

        result = select_top_features(X, y, method="variance", n_features=1)

        assert result == ["high"]
