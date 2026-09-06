import json
from pathlib import Path

import faiss
import numpy as np

from app.core.database import SessionLocal
from app.models.standard import Standard
from app.services.embedding_service import generate_embeddings


VECTOR_STORE_DIR = Path("vector_store")
INDEX_PATH = VECTOR_STORE_DIR / "standards.index"
METADATA_PATH = VECTOR_STORE_DIR / "standards_metadata.json"


def build_vector_store():
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()

    try:
        standards = (
            db.query(Standard)
            .order_by(Standard.id)
            .all()
        )

        if not standards:
            raise ValueError("No standards found in PostgreSQL.")

        print(f"Loading {len(standards)} standards from PostgreSQL...")

        texts = []

        metadata = []

        for standard in standards:

            text = standard.embedding_text

            if not text:
                text = (
                    f"{standard.is_number} | "
                    f"{standard.title} | "
                    f"{standard.domain or ''} | "
                    f"{standard.standard_type or ''}"
                )

            texts.append(text)

            metadata.append(
                {
                    "id": standard.id,
                    "is_number": standard.is_number,
                    "title": standard.title,
                    "domain": standard.domain,
                    "standard_type": standard.standard_type,
                    "status": standard.status,
                    "source_url": standard.source_url,
                }
            )

        print("Generating embeddings...")

        embeddings = generate_embeddings(texts)

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        dimension = embeddings.shape[1]

        print(f"Embedding dimension: {dimension}")

        index = faiss.IndexFlatIP(dimension)

        index.add(embeddings)

        faiss.write_index(
            index,
            str(INDEX_PATH)
        )

        with open(
            METADATA_PATH,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                metadata,
                file,
                ensure_ascii=False,
                indent=2
            )

        print()
        print("Vector store created successfully")
        print("----------------------------------")
        print(f"Standards : {len(standards)}")
        print(f"Dimension : {dimension}")
        print(f"Index     : {INDEX_PATH}")
        print(f"Metadata  : {METADATA_PATH}")

    finally:
        db.close()


if __name__ == "__main__":
    build_vector_store()