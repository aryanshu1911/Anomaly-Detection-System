import pandas as pd

from src.config import TRAIN_DATA, TEST_DATA


def load_train_data():

    if not TRAIN_DATA.exists():
        raise FileNotFoundError(f"Training dataset not found:\n{TRAIN_DATA}")

    return pd.read_parquet(TRAIN_DATA)


def load_test_data():

    if not TEST_DATA.exists():
        raise FileNotFoundError(f"Testing dataset not found:\n{TEST_DATA}")

    return pd.read_parquet(TEST_DATA)