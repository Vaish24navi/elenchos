from sqlalchemy import Column, Integer, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import relationship

from app.core.utils.database import Base

class Member(Base):
    """
    Model for member table.

    Attributes:
    id (int) : Unique identifier for member.
    org_id (int) : Unique identifier for organisation.
    user_id (int) : Unique identifier for user.
    role_id (int) : Unique identifier for role.
    status (int) : Status of member.
    settings (dict) : Settings of member.
    created_at (int) : Created timestamp of member.
    updated_at (int) : Updated timestamp of member.
    """
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey('organisation.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'), nullable=False)
    status = Column(Integer, default=0, nullable=False)
    settings = Column(JSON, default={}, nullable=True)
    created_at = Column(BigInteger, nullable=True)
    updated_at = Column(BigInteger, nullable=True)

    user = relationship('User', back_populates='memberships')
    organisation = relationship('Organisation', back_populates='memberships')
    role = relationship('Role', back_populates='memberships')
