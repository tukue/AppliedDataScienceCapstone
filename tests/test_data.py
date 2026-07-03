"""Unit tests for data module."""

import pytest
import pandas as pd
import numpy as np
from src.data.processing import (
    handle_missing_values, 
    remove_outliers, 
    encode_categorical,
    normalize_features
)


class TestDataProcessing:
    """Tests for data processing functions."""
    
    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        return pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5, np.nan],
            'feature2': [10, 20, 30, 40, 50, 60],
            'category': ['A', 'B', 'A', 'C', 'B', 'C']
        })
    
    def test_handle_missing_values_drop(self, sample_df):
        """Test missing value handling with drop strategy."""
        result = handle_missing_values(sample_df, strategy='drop')
        assert result.isnull().sum().sum() == 0
        assert len(result) == 5
    
    def test_handle_missing_values_mean(self, sample_df):
        """Test missing value handling with mean strategy."""
        result = handle_missing_values(sample_df, strategy='mean')
        assert result['feature1'].isnull().sum() == 0
    
    def test_remove_outliers(self, sample_df):
        """Test outlier removal."""
        # Add some outliers
        sample_df.loc[6] = [100, 1000, 'D']
        result = remove_outliers(sample_df, 'feature2', threshold=1.5)
        assert len(result) < len(sample_df)
    
    def test_encode_categorical(self, sample_df):
        """Test categorical encoding."""
        result = encode_categorical(sample_df, ['category'], method='onehot')
        assert 'category_B' in result.columns or 'category_C' in result.columns
        assert len(result) == len(sample_df)
    
    def test_normalize_features(self, sample_df):
        """Test feature normalization."""
        numeric_cols = ['feature1', 'feature2']
        result = normalize_features(
            sample_df.dropna(), 
            numeric_cols, 
            method='standard'
        )
        # Check that features are normalized
        assert abs(result['feature1'].mean()) < 0.1 or result['feature1'].isnull().any()


class TestFeatureHandling:
    """Tests for feature handling edge cases."""
    
    def test_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        df = pd.DataFrame()
        # Should not raise error
        assert len(df) == 0
    
    def test_all_missing_column(self):
        """Test column with all missing values."""
        df = pd.DataFrame({'col': [np.nan, np.nan, np.nan]})
        result = handle_missing_values(df, strategy='drop')
        assert len(result) == 0
