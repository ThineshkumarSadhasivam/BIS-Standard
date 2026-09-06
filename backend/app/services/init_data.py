from app.core.database import SessionLocal
from app.services.ingestion_service import load_standards


def main():

    db = SessionLocal()

    try:
        result = load_standards(db)

        print("Standards ingestion completed")
        print(f"Total records : {result['total']}")
        print(f"Inserted      : {result['inserted']}")
        print(f"Skipped       : {result['skipped']}")

    finally:
        db.close()


if __name__ == "__main__":
    main()