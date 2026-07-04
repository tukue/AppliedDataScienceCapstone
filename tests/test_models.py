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
        X, y = make_classification(n_samples=100, n_features=10, n_informative=5, random_state=42)
        X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
        y = pd.Series(y)
        return X, y

    def test_model_creation(self):
        """Test model creation."""
        trainer = ModelTrainer(model_type="random_forest")
        assert trainer.model is not None
        assert trainer.model_type == "random_forest"

    def test_unknown_model_type_falls_back_to_random_forest(self):
        """Test unknown model type falls back to a usable model."""
        trainer = ModelTrainer(model_type="unknown")

        assert trainer.model is not None
        assert trainer.model.__class__.__name__ == "RandomForestClassifier"

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
        trainer = ModelTrainer(model_type="random_forest")
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)

        trainer.train(X_train, y_train)
        # Model should be trained (has feature_importances_)
        assert hasattr(trainer.model, "feature_importances_")

    def test_model_evaluation(self, sample_data):
        """Test model evaluation."""
        X, y = sample_data
        trainer = ModelTrainer()
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        trainer.train(X_train, y_train)

        metrics = trainer.evaluate(X_test, y_test)

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics
        assert all(0 <= v <= 1 for v in metrics.values())

    def test_cross_validation(self, sample_data, monkeypatch):
        """Test cross-validation."""
        import src.models as models_module

        X, y = sample_data
        trainer = ModelTrainer()

        monkeypatch.setattr(
            models_module,
            "cross_val_score",
            lambda model, X, y, cv, scoring: np.array([0.8, 0.9, 1.0]),
        )
        cv_metrics = trainer.cross_validate(X, y, cv=5)

        assert "cv_mean" in cv_metrics
        assert "cv_std" in cv_metrics
        assert "cv_scores" in cv_metrics
        assert len(cv_metrics["cv_scores"]) == 3
        assert cv_metrics["cv_mean"] == pytest.approx(0.9)

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

        for model_type in ["random_forest", "gradient_boost", "logistic", "svm"]:
            trainer = ModelTrainer(model_type=model_type)
            X_train, X_test, y_train, y_test = trainer.split_data(X, y)
            trainer.train(X_train, y_train)
            metrics = trainer.evaluate(X_test, y_test)

            assert "accuracy" in metrics
            assert 0 <= metrics["accuracy"] <= 1

    def test_hyperparameter_tune_sets_best_model(self, sample_data, monkeypatch):
        """Test hyperparameter tuning stores a best model."""
        import src.models as models_module

        class MockGridSearch:
            """Small GridSearchCV test double."""

            def __init__(self, model, param_grid, cv, n_jobs):
                self.best_estimator_ = model
                self.best_params_ = {"n_estimators": 5}
                self.best_score_ = 0.88

            def fit(self, X_train, y_train):
                """Fit the wrapped estimator so later predictions work."""
                self.best_estimator_.set_params(n_estimators=5)
                self.best_estimator_.fit(X_train, y_train)

        X, y = sample_data
        trainer = ModelTrainer(model_type="random_forest")
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        monkeypatch.setattr(models_module, "GridSearchCV", MockGridSearch)

        trainer.hyperparameter_tune(X_train, y_train, {"n_estimators": [5]}, cv=2)

        assert trainer.best_model is not None
        predictions = trainer.predict(X_test)
        assert len(predictions) == len(X_test)

    def test_save_and_load_model(self, sample_data, tmp_path, monkeypatch):
        """Test model persistence round trip."""
        import src.models as models_module

        monkeypatch.setattr(models_module, "MODELS_DIR", tmp_path)
        X, y = sample_data
        trainer = ModelTrainer(model_type="random_forest")
        X_train, X_test, y_train, y_test = trainer.split_data(X, y)
        trainer.train(X_train, y_train)

        model_path = trainer.save_model("random_forest.joblib")
        loaded_trainer = ModelTrainer(model_type="random_forest")
        loaded_trainer.load_model("random_forest.joblib")

        assert model_path.exists()
        assert len(loaded_trainer.predict(X_test)) == len(X_test)
