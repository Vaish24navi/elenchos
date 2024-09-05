from sqlalchemy import Column, String, Integer, Boolean, JSON, BigInteger
from sqlalchemy.orm import relationship

from app.core.utils.database import Base

class Organisation(Base):
    """
    Model for organisation table.

    Attributes:
    id (int) : Unique identifier for organisation.
    name (str) : Name of organisation.
    status (int) : Status of organisation.
    personal (bool) : Personal organisation.
    settings (dict) : Settings of organisation.
    created_at (int) : Created timestamp of organisation.
    updated_at (int) : Updated timestamp of organisation.
    """

    __tablename__ = 'organisation'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(Integer, default=0, nullable=False)
    personal = Column(Boolean, default=False, nullable=True)
    settings = Column(JSON, default={}, nullable=True)
    created_at = Column(BigInteger, nullable=True)
    updated_at = Column(BigInteger, nullable=True)
 
    invites = relationship("Invite", back_populates="organisation")
    memberships = relationship('Member', back_populates='organisation')
    users = relationship('User', secondary='member', back_populates='organisations')
