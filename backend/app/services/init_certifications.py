from app.core.database import SessionLocal, Base, engine

from app.models.standard import Standard
from app.models.standard_certification import StandardCertification

from app.services.certification_ingestion_service import (
    ingest_certifications
)


def main():

    Base.metadata.create_all(
        bind=engine
    )

    db = SessionLocal()

    try:

        result = ingest_certifications(db)

        print(
            "\nCertification database initialization complete."
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