from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.core.models.member import Member
from app.core.models.role import Role

from app.core.schema.member import UpdateRole

from app.core.utils.dependencies import get_db
from app.core.utils.errors import not_found_error
from app.core.utils.middlewares import authenticate_user

router = APIRouter(
    prefix="/member",
    tags=["Members"],
    dependencies=[Depends(authenticate_user)]
)

@router.post("/update-role", status_code=status.HTTP_200_OK)
async def update_member_role(
    payload: UpdateRole, 
    db: Session = Depends(get_db)
):
    """
    Update member role.

    Args:
    payload (UpdateRole) : Payload containing member id and role name.
    db (Session) : Database session.

    Returns:
    dict : Message that member role is updated successfully.
    """
    member = db.query(Member).filter(Member.id == payload.member_id).first()
    if not member:
        raise not_found_error("Member")
 
    role = db.query(Role.id).filter(Role.id == member.role_id).first()
    if not role:
        raise not_found_error("Role")
    
    role_id = role.id
  
    db.query(Role).filter(Role.id == role_id).update({Role.name: payload.role_name})
    
    member.role_id = role_id
    db.commit()

    return {"message": "Member role updated successfully"}

@router.delete("/delete/{member_id}", status_code=status.HTTP_200_OK)
async def delete_member(
    member_id: int, 
    db: Session = Depends(get_db)
):
    """
    Delete a member.

    Args:
    member_id (int) : Member id.
    db (Session) : Database session.

    Returns:
    dict : Message that member is deleted successfully.
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise not_found_error("Member")

    db.delete(member)
    db.commit()

    return {"message": "Member deleted successfully"}
