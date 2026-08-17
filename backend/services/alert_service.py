from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.models import Alert
from typing import Optional


def save_alert(db: Session, alert_data: dict) -> Alert:
    timestamp = datetime.fromisoformat(
        alert_data["timestamp"]
    )

    alert = Alert(
        id=alert_data["alert_id"],
        timestamp=timestamp,
        prediction=alert_data["prediction"],
        probability=float(alert_data["probability"]),
        risk_score=int(alert_data["risk_score"]),
        severity=alert_data["severity"],
        priority=alert_data["priority"],
        recommendation=alert_data["recommendation"],
        status=alert_data["status"],
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert

def get_alerts(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    severity: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    prediction: Optional[str] = None,
):

    query = db.query(Alert)
    if severity:
        query = query.filter(Alert.severity == severity)
    if priority:
        query = query.filter(Alert.priority == priority)
    if status:
        query = query.filter(Alert.status == status)
    if prediction:
        query = query.filter(Alert.prediction == prediction)
        
    return query.order_by(Alert.timestamp.desc()).offset(offset).limit(limit).all()

def get_alert(db: Session, alert_id: str):
    return db.query(Alert).filter(Alert.id == alert_id).first()

def update_alert_status(db: Session, alert_id: str, new_status: str):
    alert = get_alert(db, alert_id)
    if alert:
        alert.status = new_status
        db.commit()
        db.refresh(alert)
    return alert