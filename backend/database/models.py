from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.connection import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    prediction: Mapped[str] = mapped_column(
        String,
    )

    probability: Mapped[float] = mapped_column(
        Float,
    )

    risk_score: Mapped[int] = mapped_column(
        Integer,
    )

    severity: Mapped[str] = mapped_column(
        String,
    )

    priority: Mapped[str] = mapped_column(
        String,
    )

    recommendation: Mapped[str] = mapped_column(
        String,
    )

    status: Mapped[str] = mapped_column(
        String,
        default="Open",
    )