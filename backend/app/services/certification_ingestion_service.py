import csv
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.standard import Standard
from app.models.standard_certification import StandardCertification


SEED_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "seeds"
    / "standards_certification_seed.csv"
)


def ingest_certifications(db: Session):

    if not SEED_FILE.exists():
        raise FileNotFoundError(
            f"Certification seed file not found: {SEED_FILE}"
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

            scheme = (
                row.get("scheme") or ""
            ).strip()

            certification_status = (
                row.get("certification_status") or ""
            ).strip()

            compulsory_value = (
                row.get("compulsory") or "false"
            ).strip().lower()

            compulsory = compulsory_value == "true"

            existing = (
                db.query(StandardCertification)
                .filter(
                    StandardCertification.standard_id
                    == standard.id,
                    StandardCertification.scheme
                    == scheme
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            certification = StandardCertification(
                standard_id=standard.id,
                scheme=scheme,
                certification_status=certification_status,
                compulsory=compulsory,
                product_category=(
                    row.get("product_category") or None
                ),
                qco_name=(
                    row.get("qco_name") or None
                ),
                notification_reference=(
                    row.get("notification_reference") or None
                ),
                source_document=(
                    row.get("source_document") or None
                ),
                source_url=(
                    row.get("source_url") or None
                ),
            )

            db.add(certification)

            inserted += 1

    db.commit()

    print(
        f"Certification ingestion complete: "
        f"{inserted} inserted, "
        f"{skipped} skipped"
    )

    return {
        "inserted": inserted,
        "skipped": skipped
    }