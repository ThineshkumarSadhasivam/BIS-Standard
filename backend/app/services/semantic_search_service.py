import json
import re
from pathlib import Path

import faiss
from sqlalchemy.orm import Session

from app.models.standard import Standard

from app.services.version_intelligence_service import (
    enrich_search_result,
)

from app.services.amendment_intelligence_service import (
    enrich_with_amendment_intelligence,
)

from app.services.certification_intelligence_service import (
    enrich_with_certification_intelligence,
)

from app.services.compliance_intelligence_service import (
    enrich_compliance_result,
)

from app.services.embedding_service import (
    generate_query_embedding,
)

from app.services.reranking_service import (
    rerank_results,
)

from app.services.query_understanding_service import (
    understand_query,
)


# =========================================================
# VECTOR STORE
# =========================================================

VECTOR_STORE_DIR = Path("vector_store")

INDEX_PATH = (
    VECTOR_STORE_DIR
    / "standards.index"
)

METADATA_PATH = (
    VECTOR_STORE_DIR
    / "standards_metadata.json"
)


_index = None
_metadata = None


# =========================================================
# LOAD VECTOR STORE
# =========================================================

def load_vector_store():

    global _index
    global _metadata

    # -----------------------------------------------------
    # FAISS INDEX
    # -----------------------------------------------------

    if _index is None:

        if not INDEX_PATH.exists():

            raise FileNotFoundError(
                "FAISS index not found. "
                "Run init_vector_store first."
            )

        _index = faiss.read_index(
            str(INDEX_PATH)
        )

    # -----------------------------------------------------
    # METADATA
    # -----------------------------------------------------

    if _metadata is None:

        if not METADATA_PATH.exists():

            raise FileNotFoundError(
                "Vector metadata not found."
            )

        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            _metadata = json.load(file)

    return (
        _index,
        _metadata
    )


# =========================================================
# STANDARD NUMBER NORMALIZATION
# =========================================================

def normalize_standard_number(
    value: str
) -> str:

    """
    Normalize an Indian Standard number
    for exact comparison.

    Examples:

        IS 269:2015
        is 269:2015
        IS-269:2015
        IS269:2015

    become:

        IS269:2015
    """

    if not value:
        return ""

    value = value.upper().strip()

    # Remove spaces and hyphens
    value = re.sub(
        r"[\s\-]+",
        "",
        value
    )

    return value


# =========================================================
# EXTRACT EXACT STANDARD NUMBER
# =========================================================

def extract_exact_standard_number(
    query: str
):
    """
    Detect an Indian Standard number from
    the user's search query.

    Examples:

        IS 269:2015
        is 269:2015
        IS-269:2015
        IS269:2015
    """

    if not query:
        return None

    query = query.upper().strip()

    # -----------------------------------------------------
    # Standard number pattern
    #
    # IS 269:2015
    # IS269:2015
    # IS-269:2015
    # -----------------------------------------------------

    match = re.search(
        r"\bIS\s*[-]?\s*(\d+)\s*:\s*(\d{4})\b",
        query
    )

    if match:

        number = match.group(1)
        year = match.group(2)

        return f"IS {number}:{year}"

    return None


# =========================================================
# EXACT STANDARD LOOKUP
# =========================================================

def exact_standard_search(
    db: Session,
    query: str,
    top_k: int = 5
):
    """
    Perform an exact database lookup when the user
    searches for a specific IS number.

    This avoids using semantic similarity for an
    exact identifier search.
    """

    exact_standard_number = (
        extract_exact_standard_number(
            query
        )
    )

    if not exact_standard_number:
        return None

    normalized_query = (
        normalize_standard_number(
            exact_standard_number
        )
    )

    standards = (
        db.query(Standard)
        .all()
    )

    matched_standard = None

    for standard in standards:

        normalized_db_number = (
            normalize_standard_number(
                standard.is_number
            )
        )

        if normalized_db_number == normalized_query:

            matched_standard = standard
            break

    if not matched_standard:

        return None

    # -----------------------------------------------------
    # Build result
    # -----------------------------------------------------

    result = {
        "id": matched_standard.id,
        "rank": 1,

        # Exact match
        "score": 1.0,
        "semantic_score": 1.0,
        "rerank_score": 1.0,
        "confidence": 1.0,

        "is_number": matched_standard.is_number,
        "title": matched_standard.title,
        "domain": matched_standard.domain,
        "standard_type": matched_standard.standard_type,
        "status": matched_standard.status,

        "source_authority": (
            matched_standard.source_authority
        ),

        "source_type": (
            matched_standard.source_type
        ),

        "verification_status": (
            matched_standard.verification_status
        ),

        "source_document": (
            matched_standard.source_document
        ),

        "source_url": (
            matched_standard.source_url
        ),

        # Important frontend/backend indicator
        "match_type": "EXACT_STANDARD_NUMBER",
    }

    # -----------------------------------------------------
    # Version Intelligence
    # -----------------------------------------------------

    result = enrich_search_result(
        db,
        result
    )

    # -----------------------------------------------------
    # Amendment Intelligence
    # -----------------------------------------------------

    result = (
        enrich_with_amendment_intelligence(
            db,
            result
        )
    )

    # -----------------------------------------------------
    # Certification Intelligence
    # -----------------------------------------------------

    result = (
        enrich_with_certification_intelligence(
            db,
            result
        )
    )

    # -----------------------------------------------------
    # Compliance Intelligence
    # -----------------------------------------------------

    result = enrich_compliance_result(
        db,
        result
    )

    return [result][:top_k]


# =========================================================
# SEMANTIC SEARCH
# =========================================================

def semantic_search(
    db: Session,
    query: str,
    top_k: int = 5
):

    # =====================================================
    # 0. EXACT STANDARD NUMBER SEARCH
    # =====================================================

    # If the user enters something such as:
    #
    # IS 269:2015
    #
    # perform an exact PostgreSQL lookup first.
    #
    # DO NOT send exact identifiers through FAISS.

    exact_results = exact_standard_search(
        db=db,
        query=query,
        top_k=top_k
    )

    if exact_results:

        return exact_results

    # =====================================================
    # 1. QUERY UNDERSTANDING
    # =====================================================

    query_intent = understand_query(
        query
    )

    # =====================================================
    # 2. LOAD VECTOR STORE
    # =====================================================

    index, metadata = (
        load_vector_store()
    )

    # =====================================================
    # 3. QUERY EMBEDDING
    # =====================================================

    query_embedding = (
        generate_query_embedding(
            query
        )
    )

    # =====================================================
    # 4. FAISS RETRIEVAL
    # =====================================================

    # Retrieve more candidates than requested.
    #
    # Example:
    #
    # top_k = 5
    #
    # FAISS retrieves 20 candidates.
    #
    # Reranker then selects the best 5.

    retrieval_k = min(
        max(
            top_k * 4,
            20
        ),
        index.ntotal
    )

    scores, indices = (
        index.search(
            query_embedding,
            retrieval_k
        )
    )

    # =====================================================
    # 5. BUILD CANDIDATES
    # =====================================================

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        if index_position < 0:
            continue

        standard = metadata[
            index_position
        ]

        results.append(
            {
                "id": standard["id"],

                "rank": len(results) + 1,

                "score": round(
                    float(score),
                    4
                ),

                "is_number": standard[
                    "is_number"
                ],

                "title": standard[
                    "title"
                ],

                "domain": standard[
                    "domain"
                ],

                "standard_type": standard[
                    "standard_type"
                ],

                "status": standard[
                    "status"
                ],

                "source_url": standard[
                    "source_url"
                ],
            }
        )

    # =====================================================
    # 6. HYBRID RERANKING
    # =====================================================

    reranked = rerank_results(
        query=query,
        results=results,
        query_intent=query_intent
    )

    # =====================================================
    # 7. TOP-K + INTELLIGENCE ENRICHMENT
    # =====================================================

    final_results = []

    for item in reranked[:top_k]:

        # -------------------------------------------------
        # Version Intelligence
        # -------------------------------------------------

        item = enrich_search_result(
            db,
            item
        )

        # -------------------------------------------------
        # Amendment Intelligence
        # -------------------------------------------------

        item = (
            enrich_with_amendment_intelligence(
                db,
                item
            )
        )

        # -------------------------------------------------
        # Certification Intelligence
        # -------------------------------------------------

        item = (
            enrich_with_certification_intelligence(
                db,
                item
            )
        )

        # -------------------------------------------------
        # Compliance Intelligence
        # -------------------------------------------------

        item = enrich_compliance_result(
            db,
            item
        )

        # -------------------------------------------------
        # Match Type
        # -------------------------------------------------

        item["match_type"] = (
            "SEMANTIC_MATCH"
        )

        final_results.append(
            item
        )

    # =====================================================
    # 8. RETURN
    # =====================================================

    return final_results