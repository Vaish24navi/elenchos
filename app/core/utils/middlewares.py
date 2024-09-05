from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.models.user import User

from app.core.utils.auth import decode_access_token
from app.core.utils.errors import unauthorized_error, credential_error
from app.core.utils.dependencies import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(
    request: Request, 
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    Authenticate the user.
    
    Args:
    request (Request) : Request object.
    token (str) : Access token.
    db (Session) : Database session.
    """
    if not token:
        raise unauthorized_error()
    token_data = decode_access_token(token)

    user = db.query(User).filter(User.email == token_data["sub"]).first()
    if not user:
        raise credential_error()
    
    request.state.user = user