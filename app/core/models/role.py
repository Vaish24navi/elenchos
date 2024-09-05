from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.utils.database import Base

class Role(Base):
    """
    Model for role table.
    
    Attributes:
    id (int) : Unique identifier for role.
    name (str) : Name of role.
    description (str) : Description of role.
    org_id (int) : Unique identifier for organisation.
    """
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    org_id = Column(Integer, ForeignKey('organisation.id', ondelete='CASCADE'), nullable=False)

    memberships = relationship('Member', back_populates='role')
