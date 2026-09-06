from app.core.database import SessionLocal, Base, engine

from app.models.standard import Standard
from app.models.standard_amendment import StandardAmendment

from app.services.amendment_ingestion_service import (
    ingest_amendments
)


def main():

    Base.metadata.create_all(
        bind=engine
    )

    db = SessionLocal()

    try:

        result = ingest_amendments(db)

        print(
            "\nAmendment database initialization complete."
        )

        print(
            f"Inserted : {result['inserted']}"
        )

        print(
            f"Skipped  : {result['skipped']}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()