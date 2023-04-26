from typing import Annotated
from typing import List

from pydantic import BaseModel
from pydantic import Field

from .embeded_models.basic_info import BasicInfo
from .embeded_models.state import State
from .embeded_models.date_and_time import DateAndTime
from .embeded_models.location import Location
from .embeded_models.ticket import Ticket
from .embeded_models.promocode import PromoCode


class Event(BaseModel):
    basic_info: Annotated[BasicInfo, Field(
        description="Basic information of the event",
    )]
    image_link: Annotated[str, Field(
        description="Image link of the event",
        example="https://www.example.com/image.png",
    )]
    summary: Annotated[str, Field(
        description="Summary of the event",
        example="This is a summary of the event",
    )]
    description: Annotated[str, Field(
        description="Description of the event",
        example="This is a description of the event",
    )]
    state: Annotated[State, Field(
        description="State of the event",
    )]
    date_and_time: Annotated[DateAndTime, Field(
        description="Date and time details of the event",
    )]
    location: Annotated[Location, Field(
        description="Location details of the event",
    )]
    tickets: Annotated[List[Ticket | None], Field(
        description="List of tickets available for the event",
    )]
    promo_codes: Annotated[List[PromoCode | None], Field(
        description="List of promo codes available for the event",
    )]


class EventOut(Event):
    id: Annotated[str, Field(
        description="ID of the event",
        example="a1b2c3d4e5f6g7h8i9j0",
    )]
    creator_id: Annotated[str, Field(
        description="ID of the creator of the event",
        example="3sg2c3d4e5f6g7h8i9j0",
    )]
