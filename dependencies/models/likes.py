from pydantic import BaseModel
from typing import Annotated
from pydantic import Field


event_id_type = Annotated[str,Field(
    description="ID of the event to be liked",
    example="gshacgjhvfdks",
)]

user_id_type = Annotated[str,Field(
    description="ID of the user who liked the event",
    example="gshacgjhvfdks",
)]


class LikeIn(BaseModel):
    event_id: event_id_type


class LikeDB(LikeIn):
    user_id: user_id_type
