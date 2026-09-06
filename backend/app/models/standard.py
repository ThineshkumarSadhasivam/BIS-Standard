from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Standard(Base):
    __tablename__ = "standards"

    id = Column(Integer, primary_key=True, index=True)

    is_number = Column(String(100), unique=True, nullable=False, index=True)

    title = Column(Text, nullable=False)

    domain = Column(String(100), nullable=True)

    standard_type = Column(String(100), nullable=True)

    source_authority = Column(String(100), nullable=True)

    source_type = Column(String(100), nullable=True)

    verification_status = Column(String(100), nullable=True)

    status = Column(String(100), nullable=True)

    embedding_text = Column(Text, nullable=True)

    source_document = Column(Text, nullable=True)

    source_url = Column(Text, nullable=True)

    reviewed_in = Column(String(50), nullable=True)

    amendment_count = Column(Integer, nullable=True)

    certification_status = Column(String(100), nullable=True)

    supersedes = Column(Text, nullable=True)

    superseded_by = Column(Text, nullable=True)

    metadata_rule = Column(Text, nullable=True)

    amendments = relationship(
    "StandardAmendment",
    back_populates="standard",
    cascade="all, delete-orphan"
)

    certifications = relationship(
    "StandardCertification",
    back_populates="standard",
    cascade="all, delete-orphan"
)