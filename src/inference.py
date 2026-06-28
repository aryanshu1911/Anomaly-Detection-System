import pandas as pd


def predict(model, X):
    """
    Predict attack class.

    Parameters
    ----------
    model : sklearn model
        Trained classification model.
    X : pandas.DataFrame
        Preprocessed feature dataframe.

    Returns
    -------
    numpy.ndarray
        Predicted class labels.
    """
    # Use .values if it's a DataFrame to prevent feature names warning
    X_array = X.values if hasattr(X, 'values') else X
    return model.predict(X_array)


def predict_probability(model, X):
    """
    Predict attack probability.

    Returns probability of the positive (attack) class.
    """
    X_array = X.values if hasattr(X, 'values') else X
    return model.predict_proba(X_array)[:, 1]


def predict_sample(model, sample):
    """
    Predict a single network sample.

    Parameters
    ----------
    sample : pandas.DataFrame
        DataFrame containing exactly one row.

    Returns
    -------
    dict
    """
    X_array = sample.values if hasattr(sample, 'values') else sample
    prediction = model.predict(X_array)[0]
    probability = model.predict_proba(X_array)[0][1]

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }


def predict_batch(model, X):
    """
    Predict multiple samples.

    Returns a DataFrame containing predictions
    and attack probabilities.
    """
    X_array = X.values if hasattr(X, 'values') else X
    predictions = model.predict(X_array)

    probabilities = model.predict_proba(X_array)[:, 1]

    return pd.DataFrame({
        "prediction": predictions,
        "probability": probabilities
    })