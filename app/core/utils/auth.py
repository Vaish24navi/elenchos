from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from dotenv import load_dotenv
from os import getenv

from app.core.models.user import User
from app.core.models.organisation import Organisation
from app.core.models.role import Role
from app.core.models.member import Member

from app.core.utils.dependencies import save_and_refresh
from app.core.utils.errors import conflict_error, credential_error

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    """
    Get the hashed password.
    
    Args:
    password (str) : Plain password.
    
    Returns:
    str : Hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    Verify the password with the hashed password.
    
    Args:
    plain_password (str) : Plain password.
    hashed_password (str) : Hashed password.
    
    Returns:
    bool : True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """
    Create the access token.
    
    Args:
    data (dict) : Data to be encoded in the token.
    
    Returns:
    str : Encoded token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decode the access token.

    Args:
    token (str) : Encoded token.

    Returns:
    dict : Decoded token.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
    

def create_refresh_token(data: dict):
    """
    Create the refresh token.

    Args:
    data (dict) : Data to be encoded in the token.

    Returns:
    str : Encoded token.
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_user_exists(db: Session, email: str):
    """
    Check if user exists.

    Args:
    db (Session) : Database session.
    email (str) : Email address of user.
    """

    user = db.query(User).filter(User.email == email).first()
    if user is not None:
        raise conflict_error("User")

def create_user(db: Session, email: str, password: str):
    """
    Create user.

    Args:
    db (Session) : Database session.
    email (str) : Email address of user.
    password (str) : Password of user.

    Returns:
    int : User id.
    """

    hashed_password = get_password_hash(password)
    
    user = User(email=email, password=hashed_password)
    save_and_refresh(db, user)

    return user.id
    
def create_user_resources(db: Session, user_id: int, organization_name: str):
    """
    Create user resources.

    Args:
    db (Session) : Database session.
    user_id (int) : User id.
    """

    organization = Organisation(name=organization_name, status=1)
    save_and_refresh(db, organization)

    owner_role = Role(name="owner", org_id=organization.id)
    save_and_refresh(db, owner_role)

    member_role = Role(name="member", org_id=organization.id)
    save_and_refresh(db, member_role)

    member = Member(org_id=organization.id, user_id=user_id, role_id=owner_role.id, status=1)
    save_and_refresh(db, member)

    return organization.id

def verify_user(db: Session, email: str, password: str):
    """
    Verify the user.

    Args:
    db (Session) : Database session.
    email (str) : Email address of user.
    password (str) : Password of user.

    Returns:
    User : User object.
    """

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credential_error()
    if not verify_password(password, user.password):
        raise credential_error()
    return user
