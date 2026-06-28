import joblib

from src.config import RANDOM_FOREST_MODEL, LABEL_ENCODERS, SCALER_PATH


def load_random_forest():

    if not RANDOM_FOREST_MODEL.exists():
        raise FileNotFoundError(
            f"Random Forest model not found:\n{RANDOM_FOREST_MODEL}"
        )

    return joblib.load(RANDOM_FOREST_MODEL)


def load_label_encoders():

    if not LABEL_ENCODERS.exists():
        raise FileNotFoundError(
            f"Label encoder file not found:\n{LABEL_ENCODERS}"
        )

    return joblib.load(LABEL_ENCODERS)

def load_scaler():
    if not SCALER_PATH.exists():
        raise FileNotFoundError(
            f"Scaler file not found:\n{SCALER_PATH}"
        )
    return joblib.load(SCALER_PATH)