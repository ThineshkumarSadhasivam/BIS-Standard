from typing import Optional

from pydantic import BaseModel,Field


class QueryIntent(BaseModel):
    product: Optional[str] = None
    material: Optional[str] = None

    cement_type: Optional[str] = None
    grade: Optional[str] = None

    application: Optional[str] = None
    structural_use: bool = False

    seismic_requirement: bool = False
    fire_requirement: bool = False
    electrical_requirement: bool = False
    medical_requirement: bool = False

    standard_type: Optional[str] = None

    raw_query: str

class TenderAnalysisRequest(BaseModel):
    tender_text: str = Field(
        ...,
        min_length=20,
        description="Procurement tender or specification text"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of candidate standards to retrieve"
    )