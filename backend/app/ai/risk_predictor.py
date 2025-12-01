import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
import joblib
from typing import Dict, List, Tuple
from app.models.ai_models import RiskLabel
from sklearn.dummy import DummyClassifier
import os

class RiskPredictor:
    """
    Predict risks in DPRs using XGBoost machine learning model
    """
    
    def __init__(self):
        self.models = {}
        self.feature_columns = [
            'contingency_ratio',
            'duration_months',
            'num_employees',
            'num_machinery',
            'num_materials',
            'compliance_score',
            'missing_docs_count'
        ]
        # Load trained models
        self._load_models()
    
    def _load_models(self):
        """
        Load trained models from disk
        """
        model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
        
        # Try to load XGBoost models first
        for target in ['cost_overruns', 'schedule_delays', 'resource_shortages', 'environmental_risks']:
            model_path = os.path.join(model_dir, f'xgboost_{target}_model.pkl')
            if os.path.exists(model_path):
                try:
                    self.models[target] = joblib.load(model_path)
                    print(f"Loaded XGBoost model for {target}")
                except Exception as e:
                    print(f"Failed to load XGBoost model for {target}: {e}")
        
        # If no XGBoost models, try Random Forest
        if not self.models:
            for target in ['cost_overruns', 'schedule_delays', 'resource_shortages', 'environmental_risks']:
                model_path = os.path.join(model_dir, f'randomforest_{target}_model.pkl')
                if os.path.exists(model_path):
                    try:
                        self.models[target] = joblib.load(model_path)
                        print(f"Loaded Random Forest model for {target}")
                    except Exception as e:
                        print(f"Failed to load Random Forest model for {target}: {e}")
        
        # If still no models, create fallback
        if not self.models:
            print("No trained models found. Creating fallback models.")
            self._create_fallback_models()
    
    def prepare_data(self, csv_file: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Prepare data for training from CSV file
        """
        # Load data
        df = pd.read_csv(csv_file)
        
        # Select features
        X = df[self.feature_columns]
        
        # Select targets
        y = df[['cost_overruns', 'schedule_delays', 'resource_shortages', 'environmental_risks']]
        
        # Handle missing values
        X = X.fillna(0)
        y = y.fillna(0)
        
        return X, y
    
    def train_model(self, X: pd.DataFrame, y: pd.DataFrame) -> None:
        """
        Train XGBoost models for each risk type
        """
        try:
            models = {}
            for target in y.columns:
                print(f"Training model for {target}...")
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y[target], test_size=0.2, random_state=42
                )
                
                # Create XGBoost regressor
                model = xgb.XGBRegressor(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    random_state=42
                )
                
                # Train model
                model.fit(X_train, y_train)
                models[target] = model
                
                # Evaluate model
                y_pred = model.predict(X_test)
                rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
                print(f"{target} RMSE: {rmse:.4f}")
            
            # Save models
            self.models = models
            self.save_models()
        except Exception as e:
            print(f"Error training models: {str(e)}")
            # Fall back to dummy models
            self._create_fallback_models()
    
    def predict_risks(self, features: Dict[str, float]) -> Dict[str, float]:
        """
        Predict risk scores for given features using trained models
        """
        try:
            # Convert features to DataFrame
            X = pd.DataFrame([features])
            
            # Handle missing columns
            for col in self.feature_columns:
                if col not in X.columns:
                    X[col] = 0
            
            # Reorder columns
            X = X[self.feature_columns]
            
            # Handle missing values
            X = X.fillna(0)
            
            # Predict using trained models
            risk_scores = {}
            for target, model in self.models.items():
                try:
                    prediction = model.predict(X)[0]
                    # Ensure prediction is between 0 and 1
                    risk_scores[target] = float(max(0.0, min(1.0, prediction)))
                except Exception as e:
                    print(f"Error predicting {target}: {e}")
                    risk_scores[target] = 0.5  # Default value
            
            return risk_scores
        except Exception as e:
            print(f"Error in predict_risks: {str(e)}")
            # Return default probabilities
            return {
                'cost_overruns': 0.5,
                'schedule_delays': 0.5,
                'resource_shortages': 0.5,
                'environmental_risks': 0.5
            }
    
    def save_models(self, filepath_prefix: str = "models") -> None:
        """
        Save trained models to files
        """
        try:
            os.makedirs(filepath_prefix, exist_ok=True)
            for target, model in self.models.items():
                filepath = os.path.join(filepath_prefix, f"xgboost_{target}_model.pkl")
                joblib.dump(model, filepath)
                print(f"Model for {target} saved to {filepath}")
        except Exception as e:
            print(f"Error saving models: {str(e)}")
    
    def _create_fallback_models(self) -> None:
        """
        Create simple fallback models for demonstration
        """
        try:
            # Create dummy regressors
            from sklearn.dummy import DummyRegressor
            
            targets = ['cost_overruns', 'schedule_delays', 'resource_shortages', 'environmental_risks']
            for target in targets:
                model = DummyRegressor(strategy="mean")
                # Fit with dummy data
                X_dummy = np.random.rand(100, len(self.feature_columns))
                y_dummy = np.random.rand(100) * 0.5 + 0.25  # Values between 0.25 and 0.75
                model.fit(X_dummy, y_dummy)
                self.models[target] = model
            
            print("Fallback models created successfully")
        except Exception as e:
            print(f"Error creating fallback models: {str(e)}")
            # Create minimal models
            from sklearn.dummy import DummyRegressor
            targets = ['cost_overruns', 'schedule_delays', 'resource_shortages', 'environmental_risks']
            for target in targets:
                model = DummyRegressor(strategy="constant", constant=0.5)
                X_dummy = np.array([[0]*len(self.feature_columns)])
                y_dummy = np.array([0.5])
                model.fit(X_dummy, y_dummy)
                self.models[target] = model
            print("Minimal fallback models created")

# Example usage
if __name__ == "__main__":
    # This would be used for training
    # predictor = RiskPredictor()
    # X, y = predictor.prepare_data("dpr_training_dataset.csv")
    # predictor.train_model(X, y)
    pass