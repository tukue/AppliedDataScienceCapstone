"""Model training and evaluation utilities."""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, confusion_matrix)
import joblib
from pathlib import Path
from src.logger import setup_logger
from src.config import MODELS_DIR, TEST_SIZE, RANDOM_STATE, CV_FOLDS

logger = setup_logger(__name__)


class ModelTrainer:
    """Model training and evaluation wrapper."""
    
    def __init__(self, model_type: str = "random_forest", random_state: int = RANDOM_STATE):
        """
        Initialize model trainer.
        
        Args:
            model_type: Type of model ('random_forest', 'gradient_boost', 'logistic', 'svm')
            random_state: Random state for reproducibility
        """
        self.model_type = model_type
        self.random_state = random_state
        self.model = self._create_model()
        self.best_model = None
        self.metrics = {}
        
    def _create_model(self) -> Any:
        """Create model based on type."""
        models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=self.random_state),
            'gradient_boost': GradientBoostingClassifier(n_estimators=100, random_state=self.random_state),
            'logistic': LogisticRegression(random_state=self.random_state, max_iter=1000),
            'svm': SVC(probability=True, random_state=self.random_state)
        }
        return models.get(self.model_type, models['random_forest'])
    
    def split_data(self, X: pd.DataFrame, y: pd.Series, 
                  test_size: float = TEST_SIZE) -> Tuple:
        """
        Split data into train and test sets.
        
        Args:
            X: Features
            y: Target
            test_size: Test set proportion
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state
        )
        logger.info(f"Data split: train={len(X_train)}, test={len(X_test)}")
        return X_train, X_test, y_train, y_test
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """
        Train the model.
        
        Args:
            X_train: Training features
            y_train: Training target
        """
        logger.info(f"Training {self.model_type} model")
        self.model.fit(X_train, y_train)
        logger.info("Model training completed")
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """
        Evaluate model on test set.
        
        Args:
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary of metrics
        """
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        self.metrics = metrics
        logger.info(f"Model evaluation: {metrics}")
        return metrics
    
    def cross_validate(self, X: pd.DataFrame, y: pd.Series, 
                      cv: int = CV_FOLDS) -> Dict[str, float]:
        """
        Perform cross-validation.
        
        Args:
            X: Features
            y: Target
            cv: Number of folds
            
        Returns:
            Dictionary with CV scores
        """
        scores = cross_val_score(self.model, X, y, cv=cv, scoring='f1')
        cv_metrics = {
            'cv_mean': scores.mean(),
            'cv_std': scores.std(),
            'cv_scores': scores
        }
        logger.info(f"Cross-validation scores: {cv_metrics['cv_mean']:.4f} (+/- {cv_metrics['cv_std']:.4f})")
        return cv_metrics
    
    def hyperparameter_tune(self, X_train: pd.DataFrame, y_train: pd.Series,
                           param_grid: Dict, cv: int = CV_FOLDS) -> None:
        """
        Perform hyperparameter tuning using GridSearchCV.
        
        Args:
            X_train: Training features
            y_train: Training target
            param_grid: Parameter grid for tuning
            cv: Number of folds
        """
        logger.info(f"Starting hyperparameter tuning with {len(param_grid)} parameters")
        
        grid_search = GridSearchCV(self.model, param_grid, cv=cv, n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        self.best_model = grid_search.best_estimator_
        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best CV score: {grid_search.best_score_:.4f}")
    
    def save_model(self, filename: str) -> Path:
        """
        Save trained model to file.
        
        Args:
            filename: Output filename
            
        Returns:
            Path to saved model
        """
        model_path = MODELS_DIR / filename
        model_to_save = self.best_model or self.model
        joblib.dump(model_to_save, model_path)
        logger.info(f"Model saved to {model_path}")
        return model_path
    
    def load_model(self, filename: str) -> None:
        """
        Load trained model from file.
        
        Args:
            filename: Input filename
        """
        model_path = MODELS_DIR / filename
        self.model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Features
            
        Returns:
            Predictions
        """
        model_to_use = self.best_model or self.model
        return model_to_use.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make probability predictions.
        
        Args:
            X: Features
            
        Returns:
            Probability predictions
        """
        model_to_use = self.best_model or self.model
        return model_to_use.predict_proba(X)
