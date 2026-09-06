"""Standard API schemas."""
from pydantic import BaseModel, Field


class StandardSearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        description="Procurement requirement or product description"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20
    )