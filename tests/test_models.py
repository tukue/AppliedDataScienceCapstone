"""Unit tests for model module."""

import pytest
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from src.models import ModelTrainer


class TestModelTrainer:
    """Tests for ModelTrainer class."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample classification data."""
        X, y = make_classification(
            n_samples=100, 
            n_features=10, 
            n_informative=5,
            random_state=42
        )
        X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(10)])
        y = pd.Series(y)
        return X, y
    
    def test_model_creation(self):
        """Test model creation."""
        trainer = ModelTrainer(model_type='random_forest')
        assert trainer.model is not None
        assert trainer.model_type == 'random_forest'
    
    def test_data_split(self, sample_data):
        """Test train-test split."""
        X, y = sample_data
        trainer = ModelTrainer()
        X_train, X_test, y_train, y_test = trainer.split_data(X, y, test_size=0.2)
        
        assert len(X_train) + len(X_test) == len(X)
        assert len(y_train) + len(y_test) == len(y)
        assert len(X_test) / len(X) == pytest.approx(0.2, abs=0.1)
    
    def test_model_training(self, sample_data):
        """Test model training."""
        X, y = sample_data
        trainer = ModelTrainer(model_type='random_forest')
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        
        trainer.train(X_train, y_train)
        # Model should be trained (has feature_importances_)
        assert hasattr(trainer.model, 'feature_importances_')
    
    def test_model_evaluation(self, sample_data):
        """Test model evaluation."""
        X, y = sample_data
        trainer = ModelTrainer()
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        trainer.train(X_train, y_train)
        
        metrics = trainer.evaluate(X_test, y_test)
        
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics
        assert all(0 <= v <= 1 for v in metrics.values())
    
    def test_cross_validation(self, sample_data):
        """Test cross-validation."""
        X, y = sample_data
        trainer = ModelTrainer()
        
        cv_metrics = trainer.cross_validate(X, y, cv=5)
        
        assert 'cv_mean' in cv_metrics
        assert 'cv_std' in cv_metrics
        assert 'cv_scores' in cv_metrics
        assert len(cv_metrics['cv_scores']) == 5
    
    def test_prediction(self, sample_data):
        """Test model predictions."""
        X, y = sample_data
        trainer = ModelTrainer()
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        trainer.train(X_train, y_train)
        
        predictions = trainer.predict(X_test)
        
        assert len(predictions) == len(X_test)
        assert all(pred in [0, 1] for pred in predictions)
    
    def test_probability_prediction(self, sample_data):
        """Test probability predictions."""
        X, y = sample_data
        trainer = ModelTrainer()
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        trainer.train(X_train, y_train)
        
        proba = trainer.predict_proba(X_test)
        
        assert proba.shape == (len(X_test), 2)
        assert all(0 <= p <= 1 for proba_row in proba for p in proba_row)
    
    def test_different_models(self, sample_data):
        """Test different model types."""
        X, y = sample_data
        
        for model_type in ['random_forest', 'gradient_boost', 'logistic']:
            trainer = ModelTrainer(model_type=model_type)
            X_train, X_test, y_train, y_test = trainer.split_data(X, y)
            trainer.train(X_train, y_train)
            metrics = trainer.evaluate(X_test, y_test)
            
            assert 'accuracy' in metrics
            assert 0 <= metrics['accuracy'] <= 1
