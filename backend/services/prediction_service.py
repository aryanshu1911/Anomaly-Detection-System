import pandas as pd

from src.model_loader import (
    load_random_forest,
    load_label_encoders,
    load_scaler
)

from src.preprocessing import (
    encode_features
)

from src.inference import (
    predict_sample
)

from src.risk_engine import (
    build_risk_assessment
)

from src.alert_engine import (
    build_alert
)


# Load models once when the service starts
rf = load_random_forest()
encoders = load_label_encoders()
scaler = load_scaler()


def predict_network_flow(data: dict):
    
    df = pd.DataFrame([data])

    df = encode_features(df, encoders, scaler=scaler)

    result = predict_sample(rf, df)

    assessment = build_risk_assessment(
        result["prediction"],
        result["probability"]
    )

    alert = build_alert(assessment)

    return alert