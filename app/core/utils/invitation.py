import os
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def create_invite_token(email: str, invite_id: int) -> str:
    """
    Create invite token.

    Args:
    email (str) : Email of the invitee.
    invite_id (int) : Invite ID.

    Returns:
    str : Invite token.
    """
    payload = {
        "email": email,
        "invite_id": invite_id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_invite_token(token: str) -> dict:
    """
    Verify invite token.

    Args:
    token (str) : Invite token.

    Returns:
    dict : Payload of the invite token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        return {"message": "Invalid token"}
    
