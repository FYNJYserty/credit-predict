from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import HistGradientBoostingClassifier

PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_DIR / "ml_research" / "cs-training.csv"
MODEL_PATH = PROJECT_DIR / "app" / "models" / "model.joblib"

def train(df):
    df = df.drop(columns=["Unnamed: 0"])
    X = df.drop('SeriousDlqin2yrs', axis=1)
    y = df['SeriousDlqin2yrs']

    model = HistGradientBoostingClassifier(
        learning_rate=0.05,
        max_iter=250,
        max_leaf_nodes=15,
        min_samples_leaf=40,
        l2_regularization=10.0,
        random_state=42,
    )

    print(f"Обучение на {len(X):,} строках...", flush=True)
    model.fit(X, y)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Модель сохранена: {MODEL_PATH}")

if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    train(df)
