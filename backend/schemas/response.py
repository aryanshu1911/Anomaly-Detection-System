from pydantic import BaseModel
from typing import Optional

class RiskAssessment(BaseModel):
    risk_score: int
    severity: str
    priority: str
    recommendation: str
    prediction: str
    probability: float

from pydantic import ConfigDict, Field
from datetime import datetime

class AlertResponse(BaseModel):
    alert_id: str = Field(alias="id")
    timestamp: datetime
    status: str
    prediction: str
    probability: float
    risk_score: int
    severity: str
    priority: str
    recommendation: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
