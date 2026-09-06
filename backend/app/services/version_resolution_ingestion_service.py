import csv
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.standard import Standard
from app.models.standard_version_resolution import (
    StandardVersionResolution,
)


SEED_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "seeds"
    / "standards_version_resolution_seed.csv"
)


def ingest_version_resolutions(db: Session):
    if not SEED_FILE.exists():
        raise FileNotFoundError(
            f"Version resolution seed file not found: {SEED_FILE}"
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

            referenced_is = (
                row.get("referenced_standard") or ""
            ).strip()

            current_is = (
                row.get("current_standard") or ""
            ).strip()

            relationship_type = (
                row.get("relationship") or ""
            ).strip()

            note = (
                row.get("note") or ""
            ).strip()

            if not referenced_is or not current_is:
                skipped += 1
                continue

            referenced_standard = (
                db.query(Standard)
                .filter(
                    Standard.is_number == referenced_is
                )
                .first()
            )

            current_standard = (
                db.query(Standard)
                .filter(
                    Standard.is_number == current_is
                )
                .first()
            )

            if not referenced_standard:
                print(
                    f"[WARNING] Referenced standard not found: "
                    f"{referenced_is}"
                )
                skipped += 1
                continue

            if not current_standard:
                print(
                    f"[WARNING] Current standard not found: "
                    f"{current_is}"
                )
                skipped += 1
                continue

            existing = (
                db.query(StandardVersionResolution)
                .filter(
                    StandardVersionResolution
                    .referenced_standard_id
                    == referenced_standard.id,

                    StandardVersionResolution
                    .current_standard_id
                    == current_standard.id
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            resolution = StandardVersionResolution(
                referenced_standard_id=referenced_standard.id,
                current_standard_id=current_standard.id,
                relationship=relationship_type,
                note=note,
            )

            db.add(resolution)
            inserted += 1

    db.commit()

    print(
        f"Version resolution ingestion complete: "
        f"{inserted} inserted, {skipped} skipped"
    )

    return {
        "inserted": inserted,
        "skipped": skipped,
    }