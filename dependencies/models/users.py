from datetime import datetime
from typing import Annotated

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


password_type = Annotated[str, Field(
        example="password",
        title="New password",
        description="New password of the user",
    )]
email_type = Annotated[EmailStr, Field(
        example="user@gmail.com",
        title="Email",
        description="Email of the user",
    )]
firstname_type = Annotated[str, Field(
        example="John",
        title="First name",
        description="First name of the user",
    )]
lastname_type = Annotated[str, Field(
        example="Doe",
        title="Last name",
        description="Last name of the user",
    )]
avatar_url_type = Annotated[str | None, Field(
        example="https://example.com/avatar.png",
        title="Avatar URL",
        description="URL of the user's avatar",
    )]
is_verified_type = Annotated[bool, Field(
        example=True,
        title="Is verified",
        description="Is the user verified",
    )]
last_password_update_type = Annotated[datetime, Field(
        example="2021-06-01T00:00:00.000Z",
        title="Last password update",
        description="Last time the user updated their password",
    )]
user_id_type = Annotated[str, Field(
        example="60b6d8b3e3f4f3b3f0a3f3b3",
        title="User ID",
        description="ID of the user",
    )]


class UserInSignup(BaseModel):
    email: email_type
    password: password_type
    firstname: firstname_type
    lastname: lastname_type


class UserInfo(BaseModel):
    id: user_id_type
    email: email_type
    firstname: firstname_type
    lastname: lastname_type
    avatar_url: avatar_url_type


class UserInLogin(BaseModel):
    email: email_type
    password: password_type


class UserInForgotPassword(BaseModel):
    new_password: password_type


class UserInUpdatePassword(BaseModel):
    old_password: password_type
    new_password: password_type


class UserDB(UserInSignup):
    is_verified: is_verified_type | bool = False
    avatar_url: avatar_url_type | str = ""
    last_password_update: last_password_update_type


class UserOut(UserDB):
    id: user_id_type


class UserOutLogin(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserAvatar(BaseModel):
    avatar_url: avatar_url_type


class UserToken(BaseModel):
    id: user_id_type
    email: email_type
