from sqlalchemy.orm import Session

from app.models.standard import Standard
from app.models.standard_amendment import StandardAmendment
from app.models.standard_certification import StandardCertification
from app.models.standard_version_resolution import StandardVersionResolution


def get_compliance_intelligence(
    db: Session,
    standard: Standard
):
    """
    Generate a procurement-ready compliance summary.

    Version logic:
    - Explicit version-resolution mappings take priority.
    - A standard whose own status indicates Historical/Referenced
      is never treated as the latest version.
    - Certification and amendment intelligence are evaluated against
      the resolved current standard when a current standard exists.
    """

    # -----------------------------
    # Version Check
    # -----------------------------

    version_mapping = (
        db.query(StandardVersionResolution)
        .filter(
            StandardVersionResolution.referenced_standard_id == standard.id
        )
        .first()
    )

    latest_standard = standard
    latest = True

    # First respect the standard's own lifecycle status.
    status_text = (standard.status or "").lower()

    if (
        "historical" in status_text
        or "referenced" in status_text
        or "withdrawn" in status_text
        or "superseded" in status_text
    ):
        latest = False

    # Explicit version-resolution mapping has higher priority.
    if version_mapping:
        latest = False

        resolved_standard = (
            db.query(Standard)
            .filter(
                Standard.id == version_mapping.current_standard_id
            )
            .first()
        )

        if resolved_standard:
            latest_standard = resolved_standard

    # If the standard explicitly points to a successor, also treat it
    # as non-latest. This protects records that have superseded_by metadata
    # but no separate version-resolution row.
    elif getattr(standard, "superseded_by", None):
        latest = False

        resolved_standard = (
            db.query(Standard)
            .filter(
                Standard.is_number == standard.superseded_by
            )
            .first()
        )

        if resolved_standard:
            latest_standard = resolved_standard

    # -----------------------------
    # Amendments
    # -----------------------------

    amendments = (
        db.query(StandardAmendment)
        .filter(
            StandardAmendment.standard_id == latest_standard.id
        )
        .order_by(StandardAmendment.amendment_number.desc())
        .all()
    )

    latest_amendment = amendments[0] if amendments else None

    # -----------------------------
    # Certification
    # -----------------------------

    certification = (
        db.query(StandardCertification)
        .filter(
            StandardCertification.standard_id == latest_standard.id
        )
        .first()
    )

    compulsory = False
    qco = False
    isi = False
    certification_status = "No BIS Certification Evidence"

    if certification:
        compulsory = certification.compulsory
        qco = certification.compulsory
        isi = certification.compulsory
        certification_status = certification.certification_status

    # -----------------------------
    # Recommendation
    # -----------------------------

    if latest:
        recommendation = (
            f"Use {latest_standard.is_number} for procurement."
        )
    elif latest_standard.id != standard.id:
        recommendation = (
            f"{standard.is_number} is historical/referenced. "
            f"Use {latest_standard.is_number} instead."
        )
    else:
        recommendation = (
            f"{standard.is_number} is historical/referenced, "
            "but a current successor could not be resolved "
            "from the verified dataset. Manual BIS verification "
            "is required before procurement."
        )

    if compulsory:
        recommendation += (
            " BIS Scheme-I certification and ISI Mark are mandatory."
        )

    if latest_amendment:
        recommendation += (
            f" Latest amendment year: "
            f"{latest_amendment.amendment_year}."
        )

    # -----------------------------
    # Result
    # -----------------------------

    return {
        "overall_compliance_status": certification_status,
        "qco_applicable": qco,
        "isi_mark_required": isi,
        "is_latest_version": latest,
        "recommended_standard": {
            "id": latest_standard.id,
            "is_number": latest_standard.is_number,
            "title": latest_standard.title,
        },
        "latest_amendment_year": (
            latest_amendment.amendment_year
            if latest_amendment
            else None
        ),
        "recommendation": recommendation,
    }


def enrich_compliance_result(
    db: Session,
    result: dict
):
    """
    Attach compliance intelligence to one search result.
    """

    standard = (
        db.query(Standard)
        .filter(Standard.id == result["id"])
        .first()
    )

    if not standard:
        return result

    result["compliance_intelligence"] = (
        get_compliance_intelligence(db, standard)
    )

    return result
