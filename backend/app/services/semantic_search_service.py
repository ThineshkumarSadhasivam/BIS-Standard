import json
from pathlib import Path

import faiss

from app.services.embedding_service import (
    generate_query_embedding
)

from app.services.query_understanding_service import (
    understand_query
)

from app.services.reranking_service import (
    rerank_results
)


# =========================================================
# VECTOR STORE
# =========================================================

VECTOR_STORE_DIR = Path(
    "vector_store"
)

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
# SEMANTIC SEARCH
# =========================================================

def semantic_search(
    query: str,
    top_k: int = 5
):

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
    # 7. TOP-K
    # =====================================================

    return reranked[
        :top_k
    ]