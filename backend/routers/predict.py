from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.request import PredictionRequest
from backend.services.alert_service import save_alert
from backend.services.prediction_service import predict_network_flow


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
)


@router.post("/")
async def predict(
    data: PredictionRequest,
    db: Session = Depends(get_db),
):
    raw_data = data.model_dump()

    alert = predict_network_flow(raw_data)

    save_alert(db, alert)

    return alert