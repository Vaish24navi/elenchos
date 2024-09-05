from fastapi import APIRouter,Request, BackgroundTasks, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.models.organisation import Organisation
from app.core.models.invites import Invite
from app.core.models.member import Member
from app.core.models.role import Role
from app.core.models.user import User

from app.core.schema.member import InviteMember

from app.core.utils.dependencies import get_db
from app.core.utils.invitation import create_invite_token, verify_invite_token
from app.core.utils.errors import not_found_error, unauthorized_error
from app.core.utils.middlewares import authenticate_user
from app.core.utils.mailers import send_invite_email
from app.core.utils.dependencies import save_and_refresh


router = APIRouter(
    dependencies=[Depends(authenticate_user)],
    prefix="/invitations",
    tags=["Invitations"]
)

@router.post("/send", status_code= status.HTTP_200_OK)
async def send_invite(
    background_tasks: BackgroundTasks,
    request: Request,
    payload: InviteMember, 
    db: Session = Depends(get_db)
):
    """
    Send invite to join the organisation.
    
    Args:
    background_tasks (BackgroundTasks) : Background task.
    request (Request) : Request object.
    payload (InviteMember) : InviteMember schema.
    db (Session) : Database session.
    
    Returns:
    dict : Message that invite is sent.
    """
    
    user = request.state.user

    organisation = db.query(Organisation).filter(Organisation.id == payload.organisation_id).first()
    if not organisation:
        raise not_found_error("Organisation")
    
    if user.id not in [member.user_id for member in organisation.memberships]:
        raise unauthorized_error()
    
    invite = Invite(
        email= payload.recipient_mail, 
        organisation_id= payload.organisation_id, 
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=7))
    db.add(invite)
    db.commit()

    invite_token = create_invite_token(payload.recipient_mail, invite.id)

    background_tasks.add_task(send_invite_email,payload.recipient_mail, invite_token)

    return {"message": f"Invite sent to {payload.recipient_mail}"}

@router.get("/accept", status_code= status.HTTP_200_OK)
async def accept_invite(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Accept invite to join the organisation.
    
    Args:
    request (Request) : Request object.
    db (Session) : Database session.
    
    Returns:
    dict : Message that invite is accepted
    """

    invite_token = request.query_params.get("invite_id")
    token_data = verify_invite_token(invite_token)
    invite_id = token_data.get('invite_id')
    user_email = token_data.get('email')

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        return {"message": "Please create an account to accept this invite!"}

    invite = db.query(Invite).filter(Invite.id == invite_id).first()
    if not invite or invite.status != "pending" or invite.expires_at < datetime.utcnow():
        return {"message": "Invalid or expired invite!"}
    
    membership = db.query(Member).filter(Member.user_id == request.state.user.id, Member.org_id == invite.organisation_id).first()
    if membership:
        return {"message": "You are already a member of this organisation!"}
    
    role = db.query(Role).filter(Role.name == "member").first()
    if not role:
        role = Role(name="member", description="Default role for members", org_id=invite.organisation_id)
        save_and_refresh(db, role)
    
    member = Member(user_id=user.id, org_id=invite.organisation_id, role_id=role.id, status=1)
    save_and_refresh(db,member)

    invite.status = "accepted"
    db.commit()

    return {"message": "Invite accepted successfully"}

@router.get("/cancel", status_code= status.HTTP_200_OK)
async def cancel_invite(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Cancel invite to join the organisation.

    Args:
    request (Request) : Request object.
    db (Session) : Database session.

    Returns:
    dict : Message that invite is cancelled
    """

    invite_token = request.query_params.get("invite_id")
    token_data = verify_invite_token(invite_token)
    invite_id = token_data.get('invite_id')

    invite = db.query(Invite).filter(Invite.id == invite_id).first()
    if not invite or invite.status != "pending" or invite.expires_at < datetime.utcnow():
        return {"message": "Invalid or expired invite!"}
    
    db.delete(invite)
    db.commit()

    return {"message": "Invite cancelled successfully"}
