from app.core.database import SessionLocal

from app.services.relationship_ingestion_service import (
    load_relationships
)


def main():

    db = SessionLocal()

    try:

        result = load_relationships(db)

        print("\nRelationship ingestion completed")
        print("--------------------------------")
        print(f"Total records      : {result['total']}")
        print(f"Inserted           : {result['inserted']}")
        print(f"Skipped            : {result['skipped']}")
        print(
            f"Missing standards  : "
            f"{result['missing_standards']}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()