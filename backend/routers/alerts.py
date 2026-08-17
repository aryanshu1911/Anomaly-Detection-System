from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.request import AlertUpdate
from backend.schemas.response import AlertResponse
from backend.services import alert_service

router = APIRouter(
    prefix="/alerts",
    tags=["Alert Management"],
)

@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    severity: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    prediction: Optional[str] = None,
    db: Session = Depends(get_db)
):
    alerts = alert_service.get_alerts(
        db=db,
        limit=limit,
        offset=offset,
        severity=severity,
        priority=priority,
        status=status,
        prediction=prediction
    )
    return alerts

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: str, db: Session = Depends(get_db)):
    alert = alert_service.get_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.patch("/{alert_id}", response_model=AlertResponse)
async def update_alert_status(
    alert_id: str, 
    alert_update: AlertUpdate, 
    db: Session = Depends(get_db)
):
    alert = alert_service.update_alert_status(db, alert_id, alert_update.status)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert
