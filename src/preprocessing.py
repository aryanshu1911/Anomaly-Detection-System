from src.constants import (
    DROP_COLUMNS,
    TARGET_COLUMN,
    CATEGORICAL_COLUMNS,
)


def prepare_features(df):

    X = df.drop(columns=DROP_COLUMNS)

    y = df[TARGET_COLUMN]

    return X, y


def encode_features(df, encoders):

    df = df.copy()

    for column in CATEGORICAL_COLUMNS:
        df[column] = encoders[column].transform(df[column])

    return df