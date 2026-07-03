"""Data visualization utilities."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple
from pathlib import Path
from src.config import PROJECT_ROOT
from src.logger import setup_logger

logger = setup_logger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


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
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
    logger.info(f"Figure saved to {output_path}")
    return output_path


def plot_distribution(df: pd.DataFrame, column: str, title: str = None) -> plt.Figure:
    """
    Plot distribution of a column.
    
    Args:
        df: Input DataFrame
        column: Column to plot
        title: Plot title
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    if df[column].dtype == 'object':
        df[column].value_counts().plot(kind='bar', ax=ax)
    else:
        ax.hist(df[column], bins=30, edgecolor='black')
    
    ax.set_title(title or f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    
    return fig


def plot_correlation_matrix(df: pd.DataFrame, figsize: Tuple = (12, 10)) -> plt.Figure:
    """
    Plot correlation matrix heatmap.
    
    Args:
        df: Input DataFrame
        figsize: Figure size
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, ax=ax, cbar_kws={'label': 'Correlation'})
    ax.set_title("Feature Correlation Matrix")
    plt.tight_layout()
    
    return fig


def plot_scatter(df: pd.DataFrame, x: str, y: str, title: str = None) -> plt.Figure:
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
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df[x], df[y], alpha=0.6)
    
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title or f"{x} vs {y}")
    plt.tight_layout()
    
    return fig


def plot_categorical_vs_target(df: pd.DataFrame, category_col: str, 
                               target_col: str, title: str = None) -> plt.Figure:
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
    fig, ax = plt.subplots(figsize=(10, 6))
    
    df.groupby(category_col)[target_col].mean().plot(kind='bar', ax=ax)
    ax.set_title(title or f"{category_col} vs {target_col}")
    ax.set_xlabel(category_col)
    ax.set_ylabel(f"Mean {target_col}")
    plt.tight_layout()
    
    return fig


def plot_model_performance(y_true: np.ndarray, y_pred: np.ndarray, 
                          metric_type: str = "classification") -> plt.Figure:
    """
    Plot model performance metrics.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        metric_type: 'classification' or 'regression'
        
    Returns:
        Matplotlib figure
    """
    from sklearn.metrics import confusion_matrix, classification_report
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if metric_type == "classification":
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_title("Confusion Matrix")
        ax.set_ylabel("True Label")
        ax.set_xlabel("Predicted Label")
    
    plt.tight_layout()
    return fig
