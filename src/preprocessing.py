def prepare_features(df):
    X = df.drop(columns=["label", "attack_cat"])
    y = df["label"]
    return X, y


def encode_features(df, encoders):
    df = df.copy()

    for col in ["proto", "service", "state"]:
        df[col] = encoders[col].transform(df[col])

    return df