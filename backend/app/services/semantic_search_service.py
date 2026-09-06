import json
from pathlib import Path

import faiss

from app.services.reranking_service import rerank_results
from app.services.embedding_service import generate_query_embedding


VECTOR_STORE_DIR = Path("vector_store")

INDEX_PATH = VECTOR_STORE_DIR / "standards.index"
METADATA_PATH = VECTOR_STORE_DIR / "standards_metadata.json"


_index = None
_metadata = None


def load_vector_store():
    global _index
    global _metadata

    if _index is None:

        if not INDEX_PATH.exists():
            raise FileNotFoundError(
                "FAISS index not found. "
                "Run init_vector_store first."
            )

        _index = faiss.read_index(
            str(INDEX_PATH)
        )

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

    return _index, _metadata


def semantic_search(
    query: str,
    top_k: int = 5
):

    index, metadata = load_vector_store()

    query_embedding = generate_query_embedding(query)

    # Retrieve more candidates from FAISS
    # before applying the reranker.
    retrieval_k = min(
        max(top_k * 4, 20),
        index.ntotal
    )

    scores, indices = index.search(
        query_embedding,
        retrieval_k
    )

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        if index_position < 0:
            continue

        standard = metadata[index_position]

        results.append(
            {
                "rank": len(results) + 1,
                "score": round(
                    float(score),
                    4
                ),
                "is_number": standard["is_number"],
                "title": standard["title"],
                "domain": standard["domain"],
                "standard_type": standard["standard_type"],
                "status": standard["status"],
                "source_url": standard["source_url"],
            }
        )

    # Rerank the retrieved candidates
    reranked = rerank_results(
        query,
        results
    )

    # Return only the requested number
    return reranked[:top_k]