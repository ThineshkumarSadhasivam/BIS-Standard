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


        "supersedes": standard.supersedes,

        "superseded_by": standard.superseded_by,
    }


def enrich_search_result(
    db: Session,
    result: dict
):
    """
    Add version intelligence to a semantic-search result.

    Search results currently identify standards using
    their IS number rather than database ID.
    """

    # ------------------------------------------------------------
    # 1. Get IS number from search result
    # ------------------------------------------------------------

    is_number = result.get("is_number")

    if not is_number:
        return result

    # ------------------------------------------------------------
    # 2. Find the corresponding standard in PostgreSQL
    # ------------------------------------------------------------

    standard = (
        db.query(Standard)
        .filter(
            Standard.is_number == is_number
        )
        .first()
    )

    if not standard:
        return result

    # ------------------------------------------------------------
    # 3. Resolve version intelligence
    # ------------------------------------------------------------

    version_info = resolve_standard_version(
        db,
        standard
    )

    # ------------------------------------------------------------
    # 4. Attach intelligence to search result
    # ------------------------------------------------------------

    result["version_intelligence"] = version_info

    return result