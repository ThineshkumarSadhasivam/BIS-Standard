from fastapi import FastAPI

from app.core.database import engine, Base
from app.models.standard import Standard


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="StandardsInsight API",
    description="AI-Powered Recommendation Engine for Indian Standards",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "StandardsInsight API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }