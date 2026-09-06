from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.standard import StandardSearchRequest

from app.services.semantic_search_service import semantic_search
from app.services.query_understanding_service import understand_query

from app.services.version_intelligence_service import (
    enrich_search_result,
    resolve_standard_version,
)

from app.services.amendment_intelligence_service import (
    get_amendment_history,
    enrich_with_amendment_intelligence,
)

from app.services.certification_intelligence_service import (
    get_certification_intelligence,
    enrich_with_certification_intelligence,
)

from app.services.knowledge_graph_service import (
    get_standard_relationships,
    enrich_with_knowledge_graph,
)

from app.schemas.query import TenderAnalysisRequest

from app.services.tender_analysis_service import (
    analyze_tender,
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
    # 3. Add Version + Amendment Intelligence
    # --------------------------------------------------------

    enriched_results = []

    for result in results:

        # Phase 3A
        # Version / Supersession Intelligence
        enriched_result = enrich_search_result(
            db,
            result
        )

        # Phase 3B
        # Amendment Intelligence
        enriched_result = enrich_with_amendment_intelligence(
            db,
            enriched_result
        )
        # Phase 3C
        enriched_result = enrich_with_certification_intelligence(
            db,
            enriched_result
        )
        #Phase 4
        enriched_result = enrich_with_knowledge_graph(
            db,
            enriched_result
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
        .filter(
            Standard.id == standard_id
        )
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


# ============================================================
# AMENDMENT INTELLIGENCE
# ============================================================

@router.get("/{standard_id}/amendments")
def get_standard_amendments(
    standard_id: int,
    db: Session = Depends(get_db)
):
    result = get_amendment_history(
        db,
        standard_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Standard not found"
        )

    return result

@router.get("/{standard_id}/certification")
def get_standard_certification(
    standard_id: int,
    db: Session = Depends(get_db)
):
    result = get_certification_intelligence(
        db,
        standard_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Standard not found"
        )

    return result

@router.get("/{standard_id}/relationships")
def get_standard_relationships_api(
    standard_id: int,
    db: Session = Depends(get_db)
):
    result = get_standard_relationships(
        db,
        standard_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Standard not found"
        )

    return result
@router.post("/analyze-tender")
def analyze_tender_endpoint(
    request: TenderAnalysisRequest,
    db: Session = Depends(get_db),
):
    return analyze_tender(
        db=db,
        tender_text=request.tender_text,
        top_k=request.top_k,
    )