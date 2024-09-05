from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.utils.database import Base

class Invite(Base):
    """
    Invite model.

    Attributes:
    id (int) : Invite ID.
    email (str) : Email of the invitee.
    organization_id (int) : Organization ID.
    status (str) : Invite status. (pending, accepted, rejected)
    created_at (datetime) : Created at timestamp.
    expires_at (datetime) : Expires at timestamp.
    organization (Organization) : Organization object.
    """
    __tablename__ = "invites"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    organisation_id = Column(Integer, ForeignKey('organisation.id'))
    status = Column(String, default="pending") 
    created_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False) 

    organisation = relationship("Organisation", back_populates="invites")
