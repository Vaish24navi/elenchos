from sqlalchemy import Column, String, Integer, JSON, BigInteger
from sqlalchemy.orm import relationship

from app.core.utils.database import Base

class User(Base):
    """
    Model for user table.

    Attributes:
    id (int) : Unique identifier for user.
    email (str) : Email address of user.
    password (str) : Password of user.
    profile (dict) : Profile details of user.
    status (int) : Status of user.
    settings (dict) : Settings of user.
    created_at (int) : Created timestamp of user.
    updated_at (int) : Updated timestamp of user.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    profile = Column(JSON, default={}, nullable=False)
    status = Column(Integer, default=0, nullable=False)
    settings = Column(JSON, default={}, nullable=True)
    created_at = Column(BigInteger, nullable=True)
    updated_at = Column(BigInteger, nullable=True)

    memberships = relationship('Member', back_populates='user')
    organisations = relationship('Organisation', secondary='member', back_populates='users')
