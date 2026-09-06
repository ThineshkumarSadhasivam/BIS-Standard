from fastapi import APIRouter

from app.schemas.standard import StandardSearchRequest
from app.services.semantic_search_service import semantic_search


router = APIRouter(
    prefix="/standards",
    tags=["Standards"]
)


@router.post("/search")
def search_standards(request: StandardSearchRequest):

    results = semantic_search(
        query=request.query,
        top_k=request.top_k
    )

    return {
        "query": request.query,
        "count": len(results),
        "results": results
    }