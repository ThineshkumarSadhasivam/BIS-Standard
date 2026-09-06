from sqlalchemy.orm import Session

from app.models.standard import Standard
from app.models.standard_relationship import StandardRelationship


def get_standard_relationships(
    db: Session,
    standard_id: int
):
    """
    Retrieve all standards directly connected to
    the requested standard.
    """

    standard = (
        db.query(Standard)
        .filter(Standard.id == standard_id)
        .first()
    )

    if not standard:
        return None

    outgoing = (
        db.query(StandardRelationship)
        .filter(
            StandardRelationship.source_standard_id
            == standard_id
        )
        .all()
    )

    incoming = (
        db.query(StandardRelationship)
        .filter(
            StandardRelationship.target_standard_id
            == standard_id
        )
        .all()
    )

    relationships = []

    # Relationships originating from this standard
    for relationship in outgoing:

        target = (
            db.query(Standard)
            .filter(
                Standard.id
                == relationship.target_standard_id
            )
            .first()
        )

        if not target:
            continue

        relationships.append({
            "direction": "outgoing",
            "relationship_type": (
                relationship.relationship_type
            ),
            "related_standard": {
                "id": target.id,
                "is_number": target.is_number,
                "title": target.title,
                "status": target.status
            },
            "description": relationship.description,
            "source_document": (
                relationship.source_document
            ),
            "source_url": relationship.source_url
        })

    # Relationships pointing to this standard
    for relationship in incoming:

        source = (
            db.query(Standard)
            .filter(
                Standard.id
                == relationship.source_standard_id
            )
            .first()
        )

        if not source:
            continue

        relationships.append({
            "direction": "incoming",
            "relationship_type": (
                relationship.relationship_type
            ),
            "related_standard": {
                "id": source.id,
                "is_number": source.is_number,
                "title": source.title,
                "status": source.status
            },
            "description": relationship.description,
            "source_document": (
                relationship.source_document
            ),
            "source_url": relationship.source_url
        })

    return {
        "standard_id": standard.id,
        "is_number": standard.is_number,
        "title": standard.title,
        "relationship_count": len(relationships),
        "relationships": relationships
    }


def enrich_with_knowledge_graph(
    db: Session,
    result: dict
):
    """
    Add directly related standards to a search result.
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

    graph_info = get_standard_relationships(
        db,
        standard.id
    )

    if graph_info:
        result["knowledge_graph"] = graph_info

    return result