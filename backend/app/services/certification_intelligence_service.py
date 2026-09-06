from sqlalchemy.orm import Session

from app.models.standard import Standard
from app.models.standard_certification import StandardCertification


def get_certification_intelligence(
    db: Session,
    standard_id: int
):
    standard = (
        db.query(Standard)
        .filter(Standard.id == standard_id)
        .first()
    )

    if not standard:
        return None

    certifications = (
        db.query(StandardCertification)
        .filter(
            StandardCertification.standard_id == standard_id
        )
        .all()
    )

    certification_records = []

    for certification in certifications:
        certification_records.append({
            "scheme": certification.scheme,
            "certification_status": (
                certification.certification_status
            ),
            "compulsory": certification.compulsory,
            "product_category": (
                certification.product_category
            ),
            "qco_name": certification.qco_name,
            "notification_reference": (
                certification.notification_reference
            ),
            "source_document": (
                certification.source_document
            ),
            "source_url": certification.source_url
        })

    # Determine overall procurement compliance status
    compulsory = any(
        certification.compulsory
        for certification in certifications
    )

    if compulsory:
        overall_status = "Compulsory"
    elif certifications:
        overall_status = "Certification Applicable"
    else:
        overall_status = "No Certification Evidence"

    return {
        "standard_id": standard.id,
        "is_number": standard.is_number,
        "title": standard.title,
        "overall_status": overall_status,
        "certification_count": len(certifications),
        "compulsory": compulsory,
        "certifications": certification_records
    }


def enrich_with_certification_intelligence(
    db: Session,
    result: dict
):
    """
    Add certification intelligence to an existing
    semantic-search result.

    Search results currently identify standards by
    is_number, so resolve the database ID first.
    """

    is_number = result.get("is_number")

    if not is_number:
        return result

    standard = (
        db.query(Standard)
        .filter(
            Standard.is_number == is_number
        )
        .first()
    )

    if not standard:
        return result

    certification_info = get_certification_intelligence(
        db,
        standard.id
    )

    if certification_info:
        result["certification_intelligence"] = (
            certification_info
        )

    return result