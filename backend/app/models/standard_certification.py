from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class StandardCertification(Base):
    __tablename__ = "standard_certifications"

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

    scheme = Column(
        String(100),
        nullable=False
    )

    certification_status = Column(
        String(100),
        nullable=False
    )

    compulsory = Column(
        Boolean,
        nullable=False,
        default=False
    )

    product_category = Column(
        String(255),
        nullable=True
    )

    qco_name = Column(
        String(500),
        nullable=True
    )

    notification_reference = Column(
        String(500),
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

    standard = relationship(
        "Standard",
        back_populates="certifications"
    )