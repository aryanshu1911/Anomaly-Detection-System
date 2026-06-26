import pandas as pd
from src.config import TRAIN_DATA, TEST_DATA


def load_train_data():
    """Load training dataset."""
    return pd.read_parquet(TRAIN_DATA)


def load_test_data():
    """Load testing dataset."""
    return pd.read_parquet(TEST_DATA)