import csv
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.standard import Standard
from app.models.standard_amendment import StandardAmendment


SEED_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "seeds"
    / "standards_amendments_seed.csv"
)


def ingest_amendments(db: Session):

    if not SEED_FILE.exists():
        raise FileNotFoundError(
            f"Amendment seed file not found: {SEED_FILE}"
        )

    inserted = 0
    skipped = 0

    with open(
        SEED_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            is_number = (
                row.get("is_number") or ""
            ).strip()

            if not is_number:
                skipped += 1
                continue

            standard = (
                db.query(Standard)
                .filter(
                    Standard.is_number == is_number
                )
                .first()
            )

            if not standard:
                print(
                    f"[WARNING] Standard not found: "
                    f"{is_number}"
                )
                skipped += 1
                continue

            try:
                amendment_number = int(
                    row["amendment_number"]
                )

                amendment_year = int(
                    row["amendment_year"]
                )

            except (ValueError, TypeError, KeyError):

                print(
                    f"[WARNING] Invalid amendment data "
                    f"for {is_number}"
                )

                skipped += 1
                continue

            existing = (
                db.query(StandardAmendment)
                .filter(
                    StandardAmendment.standard_id
                    == standard.id,

                    StandardAmendment.amendment_number
                    == amendment_number
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            amendment = StandardAmendment(
                standard_id=standard.id,
                amendment_number=amendment_number,
                amendment_year=amendment_year,
                source_document=None,
                source_url=None
            )

            db.add(amendment)

            inserted += 1

    db.commit()

    print(
        f"Amendment ingestion complete: "
        f"{inserted} inserted, "
        f"{skipped} skipped"
    )

    return {
        "inserted": inserted,
        "skipped": skipped
    }