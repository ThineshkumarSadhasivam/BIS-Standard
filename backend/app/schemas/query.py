from typing import Optional

from pydantic import BaseModel


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