from pydantic import BaseModel, EmailStr, Field

class UserSignIn(BaseModel):
    """
    User Sign In Schema

    Attributes:
    email (str) : Email address of user.
    password (str) : Password of user
    """

    email: EmailStr = Field(..., example="xyz@gmail.com")
    password: str = Field(..., example="password")

class UserSignUp(BaseModel):
    """
    User Sign Up Schema

    Attributes:
    email (str) : Email address of user.
    password (str) : Password of user.
    organization_name (str) : Name of organization.
    """

    email: EmailStr = Field(..., example="xyz@gmail.com")
    password: str = Field(..., example="password")
    organisation_name: str = Field(..., example="Organization Name")

class ResetPassword(BaseModel):
    """
    Reset Password Schema

    Attributes:
    email (str) : Email address of user.
    password (str) : Password of user.
    """

    email: EmailStr = Field(..., example="xyz@gmail.com")
    password: str = Field(..., example="password")

