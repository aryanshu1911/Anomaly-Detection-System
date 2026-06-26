import joblib
from src.config import RANDOM_FOREST_MODEL, LABEL_ENCODERS


def load_random_forest():
    return joblib.load(RANDOM_FOREST_MODEL)


def load_label_encoders():
    return joblib.load(LABEL_ENCODERS)