from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class StandardAmendment(Base):
    __tablename__ = "standard_amendments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    standard_id = Column(
        Integer,
        ForeignKey("standards.id"),
        nullable=False,
        index=True
    )

    amendment_number = Column(
        Integer,
        nullable=False
    )

    amendment_year = Column(
        Integer,
        nullable=False
    )

    source_document = Column(
        Text,
        nullable=True
    )

    source_url = Column(
        Text,
        nullable=True
    )

    standard = relationship(
        "Standard",
        back_populates="amendments"
    )