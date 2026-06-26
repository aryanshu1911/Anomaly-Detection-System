from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"

TRAIN_DATA = DATA_DIR / "UNSW_NB15_training-set.parquet"
TEST_DATA = DATA_DIR / "UNSW_NB15_testing-set.parquet"

RANDOM_FOREST_MODEL = MODEL_DIR / "random_forest_model.pkl"
LABEL_ENCODERS = MODEL_DIR / "label_encoders.pkl"