from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship as orm_relationship

from app.core.database import Base


class StandardVersionResolution(Base):
    __tablename__ = "standard_version_resolutions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    referenced_standard_id = Column(
        Integer,
        ForeignKey("standards.id"),
        nullable=False,
        index=True
    )

    current_standard_id = Column(
        Integer,
        ForeignKey("standards.id"),
        nullable=False,
        index=True
    )

    relationship = Column(
        String(100),
        nullable=False
    )

    note = Column(
        Text,
        nullable=True
    )

    referenced_standard = orm_relationship(
        "Standard",
        foreign_keys=[referenced_standard_id]
    )

    current_standard = orm_relationship(
        "Standard",
        foreign_keys=[current_standard_id]
    )