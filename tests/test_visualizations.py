"""Unit tests for visualization utilities."""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use("Agg")

from src.features import (  # noqa: E402
    plot_feature_importance,
    plot_categorical_vs_target,
    plot_correlation_matrix,
    plot_distribution,
    plot_model_performance,
    plot_scatter,
    save_figure,
)


class TestVisualizations:
    """Tests for professional graph output helpers."""

    def test_distribution_plot_returns_figure(self):
        """Test numeric distribution plot creation."""
        df = pd.DataFrame({"payload_mass_kg": [1000, 1200, 1500, 2000, 2500]})

        fig = plot_distribution(df, "payload_mass_kg")

        assert fig.axes[0].get_title(loc="left") == "Distribution of Payload Mass Kg"
        assert fig.axes[0].get_xlabel() == "Payload Mass Kg"

    def test_categorical_distribution_plot_limits_categories(self):
        """Test categorical distribution plot respects top_n."""
        df = pd.DataFrame({"site": list("AAABBBCCCDDDEEE")})

        fig = plot_distribution(df, "site", top_n=3)

        assert len(fig.axes[0].patches) == 3
        assert len(fig.axes[0].texts) == 3

    def test_distribution_plot_validates_column(self):
        """Test distribution plot raises a clear error for missing columns."""
        df = pd.DataFrame({"value": [1, 2, 3]})

        try:
            plot_distribution(df, "missing")
        except ValueError as exc:
            assert "Missing required column" in str(exc)
        else:
            raise AssertionError("Expected ValueError for missing column")

    def test_distribution_plot_validates_empty_data(self):
        """Test distribution plot raises a clear error for empty data."""
        df = pd.DataFrame({"value": []})

        try:
            plot_distribution(df, "value")
        except ValueError as exc:
            assert "at least one row" in str(exc)
        else:
            raise AssertionError("Expected ValueError for empty data")

    def test_correlation_matrix_returns_figure(self):
        """Test correlation matrix plot creation."""
        df = pd.DataFrame(
            {
                "payload_mass_kg": [1000, 1500, 2000],
                "flight_number": [1, 2, 3],
                "landing_success": [0, 1, 1],
            }
        )

        fig = plot_correlation_matrix(df)

        assert fig.axes[0].get_title(loc="left") == "Feature Correlation Matrix"

    def test_correlation_matrix_requires_numeric_columns(self):
        """Test correlation matrix requires at least two numeric columns."""
        df = pd.DataFrame({"site": ["A", "B"], "success": [1, 0]})

        try:
            plot_correlation_matrix(df[["site"]])
        except ValueError as exc:
            assert "at least two numeric columns" in str(exc)
        else:
            raise AssertionError("Expected ValueError for insufficient numeric columns")

    def test_scatter_plot_returns_figure(self):
        """Test scatter plot creation."""
        df = pd.DataFrame({"payload_mass_kg": [1000, 1500], "flight_number": [1, 2]})

        fig = plot_scatter(df, "flight_number", "payload_mass_kg")

        assert fig.axes[0].get_xlabel() == "Flight Number"
        assert fig.axes[0].get_ylabel() == "Payload Mass Kg"

    def test_categorical_target_plot_returns_figure(self):
        """Test categorical target plot creation."""
        df = pd.DataFrame({"site": ["A", "A", "B", "B"], "success": [1, 0, 1, 1]})

        fig = plot_categorical_vs_target(df, "site", "success")

        assert fig.axes[0].get_xlabel() == "Average Success"
        assert fig.axes[0].get_xlim()[1] > max(patch.get_width() for patch in fig.axes[0].patches)

    def test_model_performance_classification_plot_returns_figure(self):
        """Test classification performance plot creation."""
        fig = plot_model_performance(np.array([0, 1, 1]), np.array([0, 1, 0]))

        assert fig.axes[0].get_title(loc="left") == "Confusion Matrix"

    def test_model_performance_validates_lengths(self):
        """Test model performance validates matching input lengths."""
        try:
            plot_model_performance(np.array([0, 1]), np.array([1]))
        except ValueError as exc:
            assert "same length" in str(exc)
        else:
            raise AssertionError("Expected ValueError for mismatched lengths")

    def test_model_performance_residual_plot_adds_zero_line(self):
        """Test residual plot includes a zero reference line."""
        fig = plot_model_performance(
            np.array([1.0, 2.0, 3.0]), np.array([0.8, 2.1, 2.9]), metric_type="regression"
        )

        assert fig.axes[0].get_title(loc="left") == "Prediction Residuals"
        assert len(fig.axes[0].lines) >= 1

    def test_feature_importance_plot_returns_ranked_figure(self):
        """Test feature importance plot creation."""
        fig = plot_feature_importance(
            ["payload_mass_kg", "flight_number", "orbit"],
            [0.25, 0.60, 0.15],
            top_n=2,
        )

        assert fig.axes[0].get_title(loc="left") == "Top Feature Importance"
        assert len(fig.axes[0].patches) == 2

    def test_feature_importance_validates_lengths(self):
        """Test feature importance validates input lengths."""
        try:
            plot_feature_importance(["payload_mass_kg"], [0.2, 0.8])
        except ValueError as exc:
            assert "same length" in str(exc)
        else:
            raise AssertionError("Expected ValueError for mismatched lengths")

    def test_save_figure_writes_readable_png(self, tmp_path, monkeypatch):
        """Test figure saving writes to notebooks/figures."""
        import src.features as features

        monkeypatch.setattr(features, "PROJECT_ROOT", tmp_path)
        fig = plot_distribution(pd.DataFrame({"value": [1, 2, 3]}), "value")

        output_path = save_figure(fig, "professional_plot")
        image = plt.imread(output_path)

        assert output_path.exists()
        assert output_path.name == "professional_plot.png"
        assert image.size > 0
        assert image.shape[0] > 100
        assert image.shape[1] > 100

    def test_graph_functions_do_not_emit_logs(self, tmp_path, monkeypatch, capsys):
        """Test graph generation and saving do not write logs to lab output."""
        import src.features as features

        monkeypatch.setattr(features, "PROJECT_ROOT", tmp_path)
        fig = plot_distribution(
            pd.DataFrame({"payload_mass_kg": [1000, 1500, 2000]}),
            "payload_mass_kg",
        )
        save_figure(fig, "quiet_plot")

        captured = capsys.readouterr()

        assert captured.out == ""
        assert captured.err == ""
