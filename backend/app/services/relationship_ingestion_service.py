from pathlib import Path
import re

import pandas as pd
from sqlalchemy.orm import Session

from app.models.standard import Standard
from app.models.standard_relationship import StandardRelationship


CSV_PATH = Path(
    "data/seeds/standards_relationships_phase1.csv"
)


def clean_value(value):
    """Convert Pandas NaN values to Python None."""

    if pd.isna(value):
        return None

    return value


def normalize_is_number(value):
    """
    Normalize an IS number for matching.

    Examples:

        IS 3812 (Part 1)
        IS 3812 (Part 1):2013

    become:

        is 3812 (part 1)

    The year is removed ONLY for references where
    the year is not explicitly required for matching.
    """

    if value is None:
        return None

    value = str(value).strip().lower()

    # Remove year at the end, e.g. :2013
    value = re.sub(r":\d{4}$", "", value)

    # Normalize multiple spaces
    value = re.sub(r"\s+", " ", value)

    return value


def has_explicit_year(value):
    """
    Check whether the IS reference explicitly contains
    a four-digit year.

    Example:

        IS 269:2013       -> True
        IS 3812 (Part 1)  -> False
    """

    if value is None:
        return False

    value = str(value).strip()

    return bool(
        re.search(r":\d{4}$", value)
    )


def find_standard(
    db: Session,
    is_number
):
    """
    Find a standard using the following strategy:

    1. Exact match.
    2. If the reference does NOT specify a year,
       match against the standard family.

    We deliberately do NOT perform family matching
    when the reference contains an explicit year.
    """

    if is_number is None:
        return None

    is_number = str(is_number).strip()

    # ------------------------------------------------
    # STEP 1: Exact match
    # ------------------------------------------------

    standard = (
        db.query(Standard)
        .filter(
            Standard.is_number == is_number
        )
        .first()
    )

    if standard:
        return standard

    # ------------------------------------------------
    # STEP 2: Do not alter explicit versions
    # ------------------------------------------------

    if has_explicit_year(is_number):
        return None

    # ------------------------------------------------
    # STEP 3: Match version-less reference
    # ------------------------------------------------

    normalized_reference = normalize_is_number(
        is_number
    )

    standards = db.query(Standard).all()

    for standard in standards:

        normalized_standard = normalize_is_number(
            standard.is_number
        )

        if normalized_standard == normalized_reference:
            return standard

    return None


def load_relationships(db: Session):

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    inserted = 0
    skipped = 0
    missing_standards = 0

    for _, row in df.iterrows():

        source_is = clean_value(
            row["source_is"]
        )

        target_is = clean_value(
            row["target_is"]
        )

        relationship = clean_value(
            row["relationship"]
        )

        evidence = clean_value(
            row["evidence"]
        )

        # ------------------------------------------------
        # Find source standard
        # ------------------------------------------------

        source_standard = find_standard(
            db,
            source_is
        )

        # ------------------------------------------------
        # Find target standard
        # ------------------------------------------------

        target_standard = find_standard(
            db,
            target_is
        )

        # ------------------------------------------------
        # Both standards must exist
        # ------------------------------------------------

        if not source_standard or not target_standard:

            missing_standards += 1

            print(
                f"Skipping relationship: "
                f"{source_is} -> {target_is}"
            )

            continue

        # ------------------------------------------------
        # Check duplicate relationship
        # ------------------------------------------------

        existing = (
            db.query(StandardRelationship)
            .filter(
                StandardRelationship.source_standard_id
                == source_standard.id,

                StandardRelationship.target_standard_id
                == target_standard.id,

                StandardRelationship.relationship_type
                == relationship
            )
            .first()
        )

        if existing:

            skipped += 1

            continue

        # ------------------------------------------------
        # Create relationship
        # ------------------------------------------------

        new_relationship = StandardRelationship(

            source_standard_id=source_standard.id,

            target_standard_id=target_standard.id,

            relationship_type=relationship,

            description=evidence

        )

        db.add(new_relationship)

        inserted += 1

    db.commit()

    return {
        "total": len(df),
        "inserted": inserted,
        "skipped": skipped,
        "missing_standards": missing_standards
    }