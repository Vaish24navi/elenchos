from fastapi import APIRouter, status, Depends

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.models.user import User
from app.core.models.role import Role
from app.core.models.organisation import Organisation
from app.core.models.member import Member


from app.core.utils.dependencies import get_db
from app.core.utils.middlewares import authenticate_user

router = APIRouter(
    prefix="/stats",
    tags=["Stats"],
    dependencies=[Depends(authenticate_user)]
)


@router.get("/users-by-role", status_code=status.HTTP_200_OK)
async def get_users_by_role(db: Session = Depends(get_db)):
    """
    Get the number of users by role.

    Args:
    db (Session) : Database session.

    Returns:
    dict : Role wise user count.
    """

    results = db.query(Role.name, func.count(User.id)).join(User).group_by(Role.name).all()
    return {
        "message": "Role wise user count fetched successfully!",
        "role_wise_users": results
    }

@router.get("/organization-members", status_code=status.HTTP_200_OK)
async def get_organization_members(
    from_time: str = None, 
    to_time: str = None, 
    status: str = None, 
    db: Session = Depends(get_db)):
    """
    Get the number of members in each organization.

    Args:
    from_time (str) : Start time.
    to_time (str) : End time.
    status (str) : Membership status.
    db (Session) : Database session.

    Returns:
    dict : Organization wise member count.
    """

    query = db.query(Organisation.name, func.count(Member.id)).join(Member).group_by(Organisation.name)
    
    if status:
        query = query.filter(Member.status == status)
    
    if from_time and to_time:
        query = query.filter(Member.created_at.between(from_time, to_time))
    
    results = query.all()
    return {
        "message": "Organization wise member count fetched successfully!",
        "organization_wise_members": results
    }

@router.get("/organization-role-wise-users")
def get_org_role_wise_users(
    from_time: str = None, 
    to_time: str = None, 
    status: str = None, 
    db: Session = Depends(get_db)):
    """
    Get the number of users in each organization by role.

    Args:
    from_time (str) : Start time.
    to_time (str) : End time.
    status (str) : Membership status.
    db (Session) : Database session.

    Returns:
    dict : Organization and role wise
    """
    query = db.query(Organisation.name, Role.name, func.count(User.id))\
              .join(User)\
              .join(Role)\
              .group_by(Organisation.name, Role.name)
    
    if status:
        query = query.filter(Member.status == status)

    if from_time and to_time:
        query = query.filter(Member.created_at.between(from_time, to_time))
    
    results = query.all()
    return {"org_role_wise_users": results}
