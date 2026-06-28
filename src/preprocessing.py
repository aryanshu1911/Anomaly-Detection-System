import pandas as pd
from src.constants import (
    DROP_COLUMNS,
    TARGET_COLUMN,
    CATEGORICAL_COLUMNS,
)


def prepare_features(df):

    X = df.drop(columns=DROP_COLUMNS)

    y = df[TARGET_COLUMN]

    return X, y


def encode_features(df, encoders, scaler=None):
    df = df.copy()
    for column in CATEGORICAL_COLUMNS:
        df[column] = encoders[column].transform(df[column])
    
    if scaler:
        # Scale the data and reconstruct the dataframe to retain feature names
        scaled_data = scaler.transform(df)
        df = pd.DataFrame(scaled_data, columns=df.columns)
        
    return df