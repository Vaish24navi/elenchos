from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.schema.user import ResetPassword

from app.core.models.user import User

from app.core.utils.auth import get_password_hash
from app.core.utils.dependencies import get_db
from app.core.utils.mailers import send_update_pwd_email
from app.core.utils.middlewares import authenticate_user
from app.core.utils.errors import not_found_error


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(authenticate_user)]
)

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    background_tasks: BackgroundTasks,
    payload: ResetPassword, 
    db: Session = Depends(get_db)
):
    """
    Reset password for the user.
    
    Args:
    user (ResetPassword) : User details with email and new password.
    db (Session) : Database session.
    
    Returns:
    dict : Message and data.
    """
 
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if not existing_user:
        raise not_found_error("User")

    existing_user.password = get_password_hash(payload.password)
    db.commit()
    db.refresh(existing_user)

    background_tasks.add_task(send_update_pwd_email, existing_user.email)

    return {
        "message": "User password reset successfully"
    }
