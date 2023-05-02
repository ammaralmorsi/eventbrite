from pydantic import BaseModel
from typing import Annotated
from pydantic import Field


followed_user_id_type = Annotated[str,Field(
    description="ID of the user to be followed",
    example="gshacgjhvfdks",
)]

user_id_type = Annotated[str,Field(
    description="ID of the user",
    example="gshacgjhvfdks",
)]


class FollowIn(BaseModel):
    followed_user_id: followed_user_id_type


class FollowDB(FollowIn):
    user_id: user_id_type
