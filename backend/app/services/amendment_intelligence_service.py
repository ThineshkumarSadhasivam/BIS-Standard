from sqlalchemy.orm import Session

from app.models.standard import Standard
from app.models.standard_amendment import StandardAmendment


def get_amendment_history(
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

    amendments = (
        db.query(StandardAmendment)
        .filter(
            StandardAmendment.standard_id == standard_id
        )
        .order_by(
            StandardAmendment.amendment_number.asc()
        )
        .all()
    )

    history = []

    for amendment in amendments:
        history.append({
            "amendment_number": amendment.amendment_number,
            "amendment_year": amendment.amendment_year,
            "source_document": amendment.source_document,
            "source_url": amendment.source_url
        })

    latest_amendment = None

    if amendments:
        latest = amendments[-1]

        latest_amendment = {
            "amendment_number": latest.amendment_number,
            "amendment_year": latest.amendment_year
        }

    return {
        "standard_id": standard.id,
        "is_number": standard.is_number,
        "title": standard.title,
        "amendment_count": len(amendments),
        "latest_amendment": latest_amendment,
        "amendments": history
    }


def enrich_with_amendment_intelligence(
    db: Session,
    result: dict
):
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

    amendment_info = get_amendment_history(
        db,
        standard.id
    )

    if amendment_info:
        result["amendment_intelligence"] = amendment_info

    return result