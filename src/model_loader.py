import joblib

from src.config import RANDOM_FOREST_MODEL, LABEL_ENCODERS


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