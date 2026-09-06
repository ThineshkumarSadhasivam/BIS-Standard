from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.standard import StandardSearchRequest

from app.services.semantic_search_service import semantic_search
from app.services.query_understanding_service import understand_query
from app.services.version_intelligence_service import (
    enrich_search_result,
    resolve_standard_version,
)

from app.core.database import get_db
from app.models.standard import Standard


router = APIRouter(
    prefix="/standards",
    tags=["Standards"]
)


# ============================================================
# STANDARD SEARCH
# ============================================================

@router.post("/search")
def search_standards(
    request: StandardSearchRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # 1. Understand the procurement query
    # --------------------------------------------------------

    intent = understand_query(
        request.query
    )

    # --------------------------------------------------------
    # 2. Semantic retrieval + hybrid reranking
    # --------------------------------------------------------

    results = semantic_search(
        query=request.query,
        top_k=request.top_k
    )

    # --------------------------------------------------------
    # 3. Add Version Intelligence
    # --------------------------------------------------------

    enriched_results = []

    for result in results:

        enriched_result = enrich_search_result(
            db,
            result
        )

        enriched_results.append(
            enriched_result
        )

    # --------------------------------------------------------
    # 4. Return final response
    # --------------------------------------------------------

    return {
        "query": request.query,
        "intent": intent.model_dump(),
        "count": len(enriched_results),
        "results": enriched_results
    }


# ============================================================
# QUERY UNDERSTANDING
# ============================================================

@router.post("/understand")
def understand_standard_query(
    request: StandardSearchRequest
):

    intent = understand_query(
        request.query
    )

    return {
        "query": request.query,
        "intent": intent.model_dump()
    }


# ============================================================
# VERSION INTELLIGENCE
# ============================================================

@router.get("/{standard_id}/version")
def get_standard_version(
    standard_id: int,
    db: Session = Depends(get_db)
):

    standard = (
        db.query(Standard)
        .filter(Standard.id == standard_id)
        .first()
    )

    if not standard:

        raise HTTPException(
            status_code=404,
            detail="Standard not found"
        )

    return resolve_standard_version(
        db,
        standard
    )