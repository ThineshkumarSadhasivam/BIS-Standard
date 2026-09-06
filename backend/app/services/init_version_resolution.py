from app.core.database import SessionLocal, Base, engine

from app.models.standard import Standard
from app.models.standard_version_resolution import (
    StandardVersionResolution,
)

from app.services.version_resolution_ingestion_service import (
    ingest_version_resolutions,
)


def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        result = ingest_version_resolutions(db)

        print("\nVersion resolution initialization complete.")
        print(f"Inserted : {result['inserted']}")
        print(f"Skipped  : {result['skipped']}")

    finally:
        db.close()


if __name__ == "__main__":
    main()