from fastapi import APIRouter

from app.schemas.standard import StandardSearchRequest
from app.services.semantic_search_service import semantic_search
from app.services.query_understanding_service import understand_query


router = APIRouter(
    prefix="/standards",
    tags=["Standards"]
)


@router.post("/search")
def search_standards(
    request: StandardSearchRequest
):

    # Understand the procurement query
    intent = understand_query(
        request.query
    )

    # Semantic retrieval + hybrid reranking
    results = semantic_search(
        query=request.query,
        top_k=request.top_k
    )

    return {
        "query": request.query,
        "intent": intent.model_dump(),
        "count": len(results),
        "results": results
    }


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