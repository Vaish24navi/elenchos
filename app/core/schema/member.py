from pydantic import BaseModel, Field

class InviteMember(BaseModel):
    """
    Schema for inviting a member to an organisation
    
    Attributes:
    organisation_id (int): Organisation ID.
    recipient_mail (str): Email of the recipient.
    """
    organisation_id: int = Field(...,example=1)
    recipient_mail: str = Field(...,example="xyz@gmail.com")

class UpdateRole(BaseModel):
    """
    Schema for updating a member's role
    
    Attributes:
    member_id (int): Member ID.
    role_name (str): Name of the role.
    """
    member_id: int = Field(...,example=1)
    role_name: str = Field(...,example="admin")