from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.standard import Standard
from app.models.standard_relationship import StandardRelationship


# =========================================================
# RELATIONSHIP CATEGORIES
# =========================================================

RELATIONSHIP_CATEGORIES = {
    "TEST_REFERENCE": "test_references",
    "MATERIAL_REFERENCE": "material_references",
    "CONFORMITY_INPUT": "conformity_inputs",
    "REFERENCED_STANDARD": "referenced_standards",
}


def get_relationship_category(
    relationship_type: str
) -> str:
    """
    Convert the database relationship type into a
    frontend / procurement-analysis category.
    """

    return RELATIONSHIP_CATEGORIES.get(
        relationship_type,
        "other"
    )


# =========================================================
# STANDARD RELATIONSHIPS
# =========================================================

def get_standard_relationships(
    db: Session,
    standard_id: int
) -> Optional[Dict]:

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

    relationships: List[Dict] = []

    # -----------------------------------------------------
    # OUTGOING
    # -----------------------------------------------------

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

        relationship_data = {
            "direction": "outgoing",
            "relationship_type": (
                relationship.relationship_type
            ),
            "category": get_relationship_category(
                relationship.relationship_type
            ),
            "related_standard": {
                "id": target.id,
                "is_number": target.is_number,
                "title": target.title,
                "status": target.status,
            },
            "description": relationship.description,
            "source_document": (
                relationship.source_document
            ),
            "source_url": relationship.source_url,
        }

        relationships.append(
            relationship_data
        )

    # -----------------------------------------------------
    # INCOMING
    # -----------------------------------------------------

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

        relationship_data = {
            "direction": "incoming",
            "relationship_type": (
                relationship.relationship_type
            ),
            "category": get_relationship_category(
                relationship.relationship_type
            ),
            "related_standard": {
                "id": source.id,
                "is_number": source.is_number,
                "title": source.title,
                "status": source.status,
            },
            "description": relationship.description,
            "source_document": (
                relationship.source_document
            ),
            "source_url": relationship.source_url,
        }

        relationships.append(
            relationship_data
        )

    # =====================================================
    # CATEGORY GROUPING
    # =====================================================

    categories = {
        "test_references": [],
        "material_references": [],
        "conformity_inputs": [],
        "referenced_standards": [],
        "other": [],
    }

    for relationship in relationships:

        category = relationship["category"]

        if category not in categories:
            category = "other"

        categories[category].append(
            relationship
        )

    # =====================================================
    # SUMMARY
    # =====================================================

    category_counts = {
        category: len(items)
        for category, items
        in categories.items()
    }

    return {
        "standard_id": standard.id,
        "is_number": standard.is_number,
        "title": standard.title,

        # Existing field — keep for compatibility
        "relationship_count": len(
            relationships
        ),

        # Existing relationship list
        "relationships": relationships,

        # New categorized representation
        "categories": categories,

        # Useful for dashboard/report generation
        "category_counts": category_counts,
    }


# =========================================================
# SEARCH RESULT ENRICHMENT
# =========================================================

def enrich_with_knowledge_graph(
    db: Session,
    result: Dict
) -> Dict:

    is_number = result.get(
        "is_number"
    )

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
        result[
            "knowledge_graph"
        ] = graph_info

    return result