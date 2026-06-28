from src.constants import (
    LOW_THRESHOLD,
    MEDIUM_THRESHOLD,
    HIGH_THRESHOLD,
    SEVERITY_LOW,
    SEVERITY_MEDIUM,
    SEVERITY_HIGH,
    SEVERITY_CRITICAL,
    PRIORITY_P1,
    PRIORITY_P2,
    PRIORITY_P3,
    PRIORITY_P4,
)


def calculate_risk_score(probability: float) -> int:
    return round(probability * 100)


def assign_severity(risk_score: int) -> str:
    if risk_score < LOW_THRESHOLD:
        return SEVERITY_LOW

    elif risk_score < MEDIUM_THRESHOLD:
        return SEVERITY_MEDIUM

    elif risk_score < HIGH_THRESHOLD:
        return SEVERITY_HIGH

    return SEVERITY_CRITICAL


def assign_priority(severity: str) -> str:
    mapping = {
        SEVERITY_LOW: PRIORITY_P4,
        SEVERITY_MEDIUM: PRIORITY_P3,
        SEVERITY_HIGH: PRIORITY_P2,
        SEVERITY_CRITICAL: PRIORITY_P1,
    }

    return mapping[severity]


def generate_recommendation(severity: str) -> str:
    recommendations = {
        SEVERITY_LOW:
            "Monitor the connection for unusual activity.",

        SEVERITY_MEDIUM:
            "Review logs and verify network behavior.",

        SEVERITY_HIGH:
            "Investigate the endpoint and validate suspicious activity.",

        SEVERITY_CRITICAL:
            "Immediately isolate the affected host and begin incident response.",
    }

    return recommendations[severity]


def build_risk_assessment(prediction: int, probability: float) -> dict:
    risk_score = calculate_risk_score(probability)

    severity = assign_severity(risk_score)

    priority = assign_priority(severity)

    recommendation = generate_recommendation(severity)

    return {
        "prediction": "Attack" if prediction == 1 else "Normal",
        "probability": float(round(probability, 4)),
        "risk_score": risk_score,
        "severity": severity,
        "priority": priority,
        "recommendation": recommendation,
    }