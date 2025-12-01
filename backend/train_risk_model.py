# train_risk_label_model.py
import os
import json
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier

RANDOM_STATE = 42

# ❗ Use your uploaded dataset (ChatGPT environment)
DATA_PATH = "/mnt/data/dpr_training_dataset.csv"

# Clean model directory management
MODEL_DIR = "./models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Features used for training (must be present in dataset)
FEATURE_COLS = [
    'contingency_ratio',
    'duration_months',
    'num_employees',
    'num_machinery',
    'num_materials',
    'compliance_score',
    'missing_docs_count'
]

def load_and_prepare(df_path: str):
    """Loads and prepares the data for training."""
    df = pd.read_csv(df_path)

    print(f"\n📊 Dataset Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print("Columns in dataset:", df.columns.tolist())

    # Validate required columns
    missing_feats = [c for c in FEATURE_COLS if c not in df.columns]
    if missing_feats:
        raise RuntimeError(f"Missing feature columns: {missing_feats}")

    if 'risk_label' not in df.columns:
        raise RuntimeError("❌ Target column 'risk_label' not found in dataset.")

    # Drop rows with missing target
    df_clean = df.dropna(subset=['risk_label']).copy()

    # Process features
    X = df_clean[FEATURE_COLS].copy()
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

    # Process target labels
    y = df_clean['risk_label'].astype(str).copy()

    return X, y, df_clean


def build_classifier():
    """Builds XGBoost if available, else falls back to RandomForest."""
    try:
        import xgboost as xgb
        print("\n🟢 Using XGBoost Classifier")
        return xgb.XGBClassifier(
            n_estimators=400,
            max_depth=6,
            learning_rate=0.03,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=RANDOM_STATE,
            use_label_encoder=False,
            eval_metric='mlogloss',
            n_jobs=4
        )
    except Exception as e:
        print("\n🟡 XGBoost unavailable. Falling back to RandomForest.")
        return RandomForestClassifier(n_estimators=250, random_state=RANDOM_STATE)


def train_and_evaluate(X, y, clf):
    """Train and evaluate the model."""
    print("\n🔄 Encoding target labels...")
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    print("Classes found:", le.classes_)

    # Stable split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=RANDOM_STATE, stratify=y_enc
    )

    print("\n🧪 Performing 5-Fold Cross Validation...")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(clf, X, y_enc, cv=skf, scoring='accuracy')

    print(f"📈 CV Accuracy Mean: {cv_scores.mean():.4f} | Std: {cv_scores.std():.4f}")

    # Model training with early stopping (if supported)
    try:
        clf.fit(X_train, y_train, eval_set=[(X_test, y_test)],
                early_stopping_rounds=10, verbose=False)
    except TypeError:
        clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n🎯 Final Test Accuracy: {acc:.4f}\n")
    
    print("📘 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    print("\n📊 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return clf, le


def save_model(model, label_encoder):
    """Save model, encoder & training summary."""
    model_path = os.path.join(MODEL_DIR, "risk_label_model.pkl")
    le_path = os.path.join(MODEL_DIR, "risk_label_encoder.pkl")

    joblib.dump(model, model_path)
    joblib.dump(label_encoder, le_path)

    print("\n💾 Model Saved To:", model_path)
    print("💾 Label Encoder Saved To:", le_path)


def main():
    print("\n🚀 Starting Risk Label Model Training...\n")
    
    X, y, df_clean = load_and_prepare(DATA_PATH)
    clf = build_classifier()
    model, le = train_and_evaluate(X, y, clf)
    save_model(model, le)

    print("\n✨ Training Completed Successfully!")


if __name__ == "__main__":
    main()
