from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class StandardRelationship(Base):
    __tablename__ = "standard_relationships"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    source_standard_id = Column(
        Integer,
        ForeignKey("standards.id"),
        nullable=False,
        index=True
    )

    target_standard_id = Column(
        Integer,
        ForeignKey("standards.id"),
        nullable=False,
        index=True
    )

    relationship_type = Column(
        String(100),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    source_document = Column(
        Text,
        nullable=True
    )

    source_url = Column(
        Text,
        nullable=True
    )

    source_standard = relationship(
        "Standard",
        foreign_keys=[source_standard_id]
    )

    target_standard = relationship(
        "Standard",
        foreign_keys=[target_standard_id]
    )