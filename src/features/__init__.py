"""Data visualization utilities."""

import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Sequence, Tuple
from pathlib import Path
from src.config import PROJECT_ROOT

PRIMARY_COLOR = "#1F77B4"
ACCENT_COLOR = "#FF7F0E"
SEQUENTIAL_CMAP = "YlGnBu"
DIVERGING_CMAP = "vlag"
BACKGROUND_COLOR = "#FFFFFF"
GRID_COLOR = "#E6E8EB"
TEXT_COLOR = "#202124"

sns.set_theme(
    context="notebook",
    style="whitegrid",
    palette=[PRIMARY_COLOR, ACCENT_COLOR, "#2CA02C", "#D62728", "#9467BD", "#8C564B"],
)
plt.rcParams.update(
    {
        "figure.figsize": (12, 7),
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.facecolor": BACKGROUND_COLOR,
        "axes.facecolor": BACKGROUND_COLOR,
        "axes.edgecolor": "#DADCE0",
        "axes.labelcolor": TEXT_COLOR,
        "axes.titlecolor": TEXT_COLOR,
        "axes.titlesize": 16,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "xtick.color": TEXT_COLOR,
        "ytick.color": TEXT_COLOR,
        "font.size": 11,
        "legend.frameon": False,
    }
)


def _format_label(label: str) -> str:
    """Convert technical column names into readable plot labels."""
    return str(label).replace("_", " ").strip().title()


def _validate_columns(df: pd.DataFrame, columns: Sequence[str]) -> None:
    """Raise a clear error when a plot references missing columns."""
    missing_columns = [column for column in columns if column not in df.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required column(s): {missing}")


def _validate_non_empty(df: pd.DataFrame) -> None:
    """Raise a clear error when a plot has no data to render."""
    if df.empty:
        raise ValueError("Plot data must contain at least one row.")


def _style_axes(ax: plt.Axes) -> None:
    """Apply consistent professional styling to a Matplotlib axis."""
    ax.grid(axis="y", color=GRID_COLOR, linewidth=0.8)
    ax.grid(axis="x", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#DADCE0")
    ax.spines["bottom"].set_color("#DADCE0")
    ax.tick_params(axis="both", labelsize=10)


def _finalize_figure(fig: plt.Figure, ax: plt.Axes, widen_x_for_labels: bool = False) -> plt.Figure:
    """Apply shared finishing touches before returning a figure."""
    if widen_x_for_labels and ax.patches:
        current_left, current_right = ax.get_xlim()
        max_width = max(patch.get_width() for patch in ax.patches)
        padding = max(abs(max_width) * 0.12, 0.1)
        ax.set_xlim(current_left, max(current_right, max_width + padding))

    _style_axes(ax)
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        fig.tight_layout()
    return fig


def _annotate_horizontal_bars(ax: plt.Axes, value_format: str = "{:.2f}") -> None:
    """Annotate horizontal bars without overwhelming the chart."""
    if not ax.patches:
        return

    max_width = max(patch.get_width() for patch in ax.patches)
    offset = max_width * 0.01 if max_width else 0.01

    for patch in ax.patches:
        width = patch.get_width()
        label = value_format.format(width)
        ax.text(
            width + offset,
            patch.get_y() + patch.get_height() / 2,
            label,
            va="center",
            ha="left",
            color=TEXT_COLOR,
            fontsize=9,
        )


def save_figure(fig: plt.Figure, filename: str, dpi: int = 300) -> Path:
    """
    Save figure to file.

    Args:
        fig: Matplotlib figure object
        filename: Output filename
        dpi: Resolution

    Returns:
        Path to saved figure
    """
    figures_dir = PROJECT_ROOT / "notebooks/figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    output_path = figures_dir / filename
    if not output_path.suffix:
        output_path = output_path.with_suffix(".png")

    fig.savefig(
        output_path,
        dpi=dpi,
        bbox_inches="tight",
        facecolor=BACKGROUND_COLOR,
        transparent=False,
    )
    return output_path


def plot_distribution(
    df: pd.DataFrame, column: str, title: Optional[str] = None, top_n: int = 15
) -> plt.Figure:
    """
    Plot distribution of a column.

    Args:
        df: Input DataFrame
        column: Column to plot
        title: Plot title
        top_n: Maximum categories to show for categorical columns

    Returns:
        Matplotlib figure
    """
    _validate_columns(df, [column])
    _validate_non_empty(df)

    fig, ax = plt.subplots(figsize=(11, 6))
    label = _format_label(column)

    if pd.api.types.is_object_dtype(df[column]) or pd.api.types.is_categorical_dtype(df[column]):
        counts = df[column].value_counts().head(top_n).sort_values()
        colors = sns.color_palette(SEQUENTIAL_CMAP, n_colors=len(counts))
        ax.barh(counts.index.astype(str), counts.values, color=colors)
        ax.set_xlabel("Count")
        ax.set_ylabel(label)
        _annotate_horizontal_bars(ax, "{:.0f}")
    else:
        sns.histplot(
            data=df,
            x=column,
            bins=30,
            kde=True,
            color=PRIMARY_COLOR,
            edgecolor=BACKGROUND_COLOR,
            linewidth=0.7,
            ax=ax,
        )
        ax.set_xlabel(label)
        ax.set_ylabel("Frequency")

    ax.set_title(title or f"Distribution of {label}", loc="left", pad=14)

    return _finalize_figure(
        fig,
        ax,
        widen_x_for_labels=pd.api.types.is_object_dtype(df[column])
        or pd.api.types.is_categorical_dtype(df[column]),
    )


def plot_correlation_matrix(df: pd.DataFrame, figsize: Tuple = (12, 10)) -> plt.Figure:
    """
    Plot correlation matrix heatmap.

    Args:
        df: Input DataFrame
        figsize: Figure size

    Returns:
        Matplotlib figure
    """
    _validate_non_empty(df)
    numeric_df = df.select_dtypes(include=[np.number]).rename(columns=_format_label)
    if numeric_df.shape[1] < 2:
        raise ValueError("Correlation matrix requires at least two numeric columns.")

    fig, ax = plt.subplots(figsize=figsize)
    corr_matrix = numeric_df.corr()

    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap=DIVERGING_CMAP,
        center=0,
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        linecolor=BACKGROUND_COLOR,
        square=True,
        ax=ax,
        cbar_kws={"label": "Correlation"},
    )
    ax.set_title("Feature Correlation Matrix", loc="left", pad=14)
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", rotation=0)
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    fig.tight_layout()

    return fig


def plot_scatter(df: pd.DataFrame, x: str, y: str, title: Optional[str] = None) -> plt.Figure:
    """
    Plot scatter plot.

    Args:
        df: Input DataFrame
        x: X-axis column
        y: Y-axis column
        title: Plot title

    Returns:
        Matplotlib figure
    """
    _validate_columns(df, [x, y])
    _validate_non_empty(df)

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.scatterplot(
        data=df,
        x=x,
        y=y,
        color=PRIMARY_COLOR,
        edgecolor=BACKGROUND_COLOR,
        linewidth=0.5,
        alpha=0.78,
        s=70,
        ax=ax,
    )

    ax.set_xlabel(_format_label(x))
    ax.set_ylabel(_format_label(y))
    ax.set_title(title or f"{_format_label(y)} vs {_format_label(x)}", loc="left", pad=14)

    return _finalize_figure(fig, ax)


def plot_categorical_vs_target(
    df: pd.DataFrame, category_col: str, target_col: str, title: Optional[str] = None
) -> plt.Figure:
    """
    Plot categorical variable against target.

    Args:
        df: Input DataFrame
        category_col: Categorical column
        target_col: Target column
        title: Plot title

    Returns:
        Matplotlib figure
    """
    _validate_columns(df, [category_col, target_col])
    _validate_non_empty(df)

    fig, ax = plt.subplots(figsize=(11, 6))

    summary = df.groupby(category_col, observed=False)[target_col].mean().sort_values()
    colors = sns.color_palette(SEQUENTIAL_CMAP, n_colors=len(summary))
    ax.barh(summary.index.astype(str), summary.values, color=colors)
    _annotate_horizontal_bars(ax, "{:.2f}")
    ax.set_title(
        title or f"Average {_format_label(target_col)} by {_format_label(category_col)}",
        loc="left",
        pad=14,
    )
    ax.set_xlabel(f"Average {_format_label(target_col)}")
    ax.set_ylabel(_format_label(category_col))

    return _finalize_figure(fig, ax, widen_x_for_labels=True)


def plot_model_performance(
    y_true: np.ndarray, y_pred: np.ndarray, metric_type: str = "classification"
) -> plt.Figure:
    """
    Plot model performance metrics.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        metric_type: 'classification' or 'regression'

    Returns:
        Matplotlib figure
    """
    from sklearn.metrics import confusion_matrix

    if len(y_true) == 0 or len(y_pred) == 0:
        raise ValueError("y_true and y_pred must contain at least one value.")
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    fig, ax = plt.subplots(figsize=(8, 6))

    if metric_type == "classification":
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap=SEQUENTIAL_CMAP,
            linewidths=0.75,
            linecolor=BACKGROUND_COLOR,
            cbar=False,
            ax=ax,
        )
        ax.set_title("Confusion Matrix", loc="left", pad=14)
        ax.set_ylabel("True Label")
        ax.set_xlabel("Predicted Label")
        ax.grid(False)
    else:
        residuals = np.asarray(y_true) - np.asarray(y_pred)
        sns.histplot(residuals, bins=30, kde=True, color=PRIMARY_COLOR, ax=ax)
        ax.axvline(0, color=ACCENT_COLOR, linestyle="--", linewidth=1.5)
        ax.set_title("Prediction Residuals", loc="left", pad=14)
        ax.set_xlabel("Residual")
        ax.set_ylabel("Frequency")

    return _finalize_figure(fig, ax)


def plot_feature_importance(
    feature_names: Sequence[str],
    importance_values: Sequence[float],
    title: Optional[str] = None,
    top_n: int = 15,
) -> plt.Figure:
    """
    Plot model feature importance values as a ranked horizontal bar chart.

    Args:
        feature_names: Feature names in the same order as importance values
        importance_values: Numeric feature importance values
        title: Plot title
        top_n: Maximum features to show

    Returns:
        Matplotlib figure
    """
    if len(feature_names) != len(importance_values):
        raise ValueError("feature_names and importance_values must have the same length.")
    if len(feature_names) == 0:
        raise ValueError("At least one feature is required to plot feature importance.")

    importance_df = (
        pd.DataFrame({"feature": feature_names, "importance": importance_values})
        .sort_values("importance", ascending=False)
        .head(top_n)
        .sort_values("importance")
    )

    fig, ax = plt.subplots(figsize=(11, 6))
    colors = sns.color_palette(SEQUENTIAL_CMAP, n_colors=len(importance_df))
    ax.barh(
        importance_df["feature"].map(_format_label),
        importance_df["importance"],
        color=colors,
    )
    _annotate_horizontal_bars(ax, "{:.3f}")
    ax.set_title(title or "Top Feature Importance", loc="left", pad=14)
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")

    return _finalize_figure(fig, ax, widen_x_for_labels=True)
