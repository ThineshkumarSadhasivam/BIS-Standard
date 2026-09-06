from sqlalchemy.orm import Session

from app.models.standard import Standard
from app.models.standard_version_resolution import (
    StandardVersionResolution,
)


def resolve_standard_version(
    db: Session,
    standard: Standard
):
    """
    Resolve the version status of a standard.

    Priority:
    1. Explicit version-resolution mapping
    2. Direct superseded_by metadata
    3. Current candidate / existing status
    """

    # ============================================================
    # 1. CHECK EXPLICIT VERSION-RESOLUTION MAPPING
    # ============================================================

    resolution = (
        db.query(StandardVersionResolution)
        .filter(
            StandardVersionResolution.referenced_standard_id
            == standard.id
        )
        .first()
    )

    if resolution:

        current_standard = (
            db.query(Standard)
            .filter(
                Standard.id
                == resolution.current_standard_id
            )
            .first()
        )

        return {
            "retrieved_standard": {
                "id": standard.id,
                "is_number": standard.is_number,
                "title": standard.title,
                "status": standard.status,
            },

            "version_status": (
                "Historical / Referenced Version"
            ),

            "current_standard": (
                {
                    "id": current_standard.id,
                    "is_number": current_standard.is_number,
                    "title": current_standard.title,
                    "status": current_standard.status,
                }
                if current_standard
                else None
            ),

            "relationship": resolution.relationship,

            "resolution_note": resolution.note,

            "amendment_count": standard.amendment_count,

            "supersedes": standard.supersedes,

            "superseded_by": standard.superseded_by,
        }

    # ============================================================
    # 2. CHECK DIRECT SUPERSESSION INFORMATION
    # ============================================================

    if standard.superseded_by:

        current_standard = (
            db.query(Standard)
            .filter(
                Standard.is_number
                == standard.superseded_by
            )
            .first()
        )

        return {
            "retrieved_standard": {
                "id": standard.id,
                "is_number": standard.is_number,
                "title": standard.title,
                "status": standard.status,
            },

            "version_status": "Superseded",

            "current_standard": (
                {
                    "id": current_standard.id,
                    "is_number": current_standard.is_number,
                    "title": current_standard.title,
                    "status": current_standard.status,
                }
                if current_standard
                else None
            ),

            "relationship": "SUPERSEDED BY",

            "resolution_note": (
                f"{standard.is_number} is superseded by "
                f"{standard.superseded_by}."
            ),

            "amendment_count": standard.amendment_count,

            "supersedes": standard.supersedes,

            "superseded_by": standard.superseded_by,
        }

    # ============================================================
    # 3. NO VERSION-RESOLUTION INFORMATION
    # ============================================================

    return {
        "retrieved_standard": {
            "id": standard.id,
            "is_number": standard.is_number,
            "title": standard.title,
            "status": standard.status,
        },

        "version_status": standard.status,

        "current_standard": None,

        "relationship": None,

        "resolution_note": None,

        "amendment_count": standard.amendment_count,

        "supersedes": standard.supersedes,

        "superseded_by": standard.superseded_by,
    }


def enrich_search_result(
    db: Session,
    result: dict
):
    """
    Add version intelligence to a semantic-search result.
    """

    standard_id = result.get("id")

    if not standard_id:
        return result

    standard = (
        db.query(Standard)
        .filter(Standard.id == standard_id)
        .first()
    )

    if not standard:
        return result

    version_info = resolve_standard_version(
        db,
        standard
    )

    result["version_intelligence"] = version_info

    return result