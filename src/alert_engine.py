from datetime import datetime, UTC
from uuid import uuid4

from src.constants import (
    STATUS_OPEN,
    ALERT_PREFIX
)


def generate_alert_id() -> str:
    return f"{ALERT_PREFIX}-{uuid4().hex[:8].upper()}"


def current_timestamp() -> str:
    return datetime.now(UTC).isoformat()


def build_alert(assessment: dict) -> dict:
    return {
        "alert_id": generate_alert_id(),
        "timestamp": current_timestamp(),
        "status": STATUS_OPEN,

        **assessment
    }