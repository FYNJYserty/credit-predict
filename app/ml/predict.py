from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model.joblib"
THRESHOLD = 0.5


@lru_cache(maxsize=1)
def load_model():
    return joblib.load(MODEL_PATH)


def predict_risk(features):
    model = load_model()
    # Названия и порядок столбцов берём из сохранённой модели.
    row = pd.DataFrame([features]).loc[:, model.feature_names_in_]
    probability = float(model.predict_proba(row)[0, 1])
    return {
        "probability": probability,
        "threshold": THRESHOLD,
        "high_risk": probability >= THRESHOLD,
    }
