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

    if version_mapping:
        latest = False

        latest_standard = (
            db.query(Standard)
            .filter(Standard.id == version_mapping.current_standard_id)
            .first()
        )

    # -----------------------------
    # Amendments
    # -----------------------------

    amendments = (
        db.query(StandardAmendment)
        .filter(StandardAmendment.standard_id == latest_standard.id)
        .order_by(StandardAmendment.amendment_number.desc())
        .all()
    )

    latest_amendment = amendments[0] if amendments else None

    # -----------------------------
    # Certification
    # -----------------------------

    certification = (
        db.query(StandardCertification)
        .filter(StandardCertification.standard_id == latest_standard.id)
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

    recommendation = (
        f"Use {latest_standard.is_number} for procurement."
    )

    if not latest:
        recommendation = (
            f"{standard.is_number} is historical. "
            f"Use {latest_standard.is_number} instead."
        )

    if compulsory:
        recommendation += (
            " BIS Scheme-I certification and ISI Mark are mandatory."
        )

    if latest_amendment:
        recommendation += (
            f" Latest amendment year: {latest_amendment.amendment_year}."
        )

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