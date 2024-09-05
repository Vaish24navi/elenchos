from fastapi import APIRouter, status, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.core.schema.user import UserSignIn, UserSignUp

from app.core.models.user import User
from app.core.models.organisation import Organisation
from app.core.models.role import Role
from app.core.models.member import Member

from app.core.utils.auth import (
    create_access_token, 
    create_refresh_token,
    create_user,
    create_user_resources,
    verify_user,
    check_user_exists,
)
from app.core.utils.dependencies import get_db
from app.core.utils.mailers import send_login_email

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/sign-in", status_code=status.HTTP_200_OK)
async def sign_in(
    background_tasks: BackgroundTasks,
    payload: UserSignIn, 
    db: Session = Depends(get_db),  
):
    """
    Sign in the user.
    
    Args:
    user (UserSignIn) : User sign in details.
    db (Session) : Database session.
    
    Returns:
    dict : Access token, refresh token and token type.
    """
    user = verify_user(db, payload.email, payload.password)
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    background_tasks.add_task(send_login_email, user.email)

    return {
        "message": "User signed in successfully",
        "data": {
            "access_token": access_token, 
            "refresh_token": refresh_token, 
            "token_type": "bearer"
        }
    }


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up(
    payload: UserSignUp, 
    db: Session = Depends(get_db)
):
    """
    Sign up the user.

    Args:
    user (UserSignUp) : User sign up details.
    db (Session) : Database session.

    Returns:
    dict : Message and data.
    """

    check_user_exists(db, payload.email)
    
    user_id = create_user(db, payload.email, payload.password)
    organization_id = create_user_resources(db, user_id, payload.organisation_name)
    
    return {
        "message": "User signed up successfully", 
        "data": {
            "user_id": user_id, 
            "organization_id": organization_id
        }
    }
