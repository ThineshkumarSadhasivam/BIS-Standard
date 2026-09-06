from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.models.standard import Standard


CSV_PATH = Path("data/seeds/standards_master_phase1.csv")


def clean_value(value):
    """
    Convert Pandas NaN/empty values into Python None.
    PostgreSQL stores None as SQL NULL.
    """
    if pd.isna(value):
        return None

    return value


def load_standards(db: Session):

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():

        is_number = clean_value(row["is_number"])

        existing = (
            db.query(Standard)
            .filter(Standard.is_number == is_number)
            .first()
        )

        if existing:
            skipped += 1
            continue

        standard = Standard(
            is_number=is_number,
            title=clean_value(row["title"]),
            domain=clean_value(row["domain"]),
            standard_type=clean_value(row["standard_type"]),
            source_authority=clean_value(row["source_authority"]),
            source_type=clean_value(row["source_type"]),
            verification_status=clean_value(
                row["verification_status"]
            ),
            status=clean_value(row["status"]),
            embedding_text=clean_value(
                row["embedding_text"]
            ),
            source_document=clean_value(
                row["source_document"]
            ),
            source_url=clean_value(row["source_url"]),
            reviewed_in=clean_value(row["reviewed_in"]),
            amendment_count=clean_value(
                row["amendment_count"]
            ),
            certification_status=clean_value(
                row["certification_status"]
            ),
            supersedes=clean_value(row["supersedes"]),
            superseded_by=clean_value(
                row["superseded_by"]
            ),
            metadata_rule=clean_value(
                row["metadata_rule"]
            ),
        )

        db.add(standard)
        inserted += 1

    db.commit()

    return {
        "inserted": inserted,
        "skipped": skipped,
        "total": len(df)
    }