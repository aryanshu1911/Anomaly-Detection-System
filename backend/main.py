import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI

from backend.database.connection import Base, engine
from backend.database import models

from backend.routers.health import router as health_router
from backend.routers.predict import router as predict_router
from backend.routers.alerts import router as alerts_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SentinelAI",
    description="AI-Powered Network Anomaly Detection & Security Operations Platform",
    version="1.0.0",
)


app.include_router(health_router)
app.include_router(predict_router)
app.include_router(alerts_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)