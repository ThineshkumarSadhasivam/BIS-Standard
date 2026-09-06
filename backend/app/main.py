from fastapi import FastAPI

from app.core.database import engine, Base

from app.models.standard import Standard
from app.models.standard_relationship import StandardRelationship

from app.api.routes.standards import router as standards_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="StandardsInsight API",
    description="AI-Powered Recommendation Engine for Indian Standards",
    version="1.0.0",
)


# Register Standards API routes
app.include_router(standards_router)


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