from typing import Annotated
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class DateAndTime(BaseModel):
    start_date_time: Annotated[datetime, Field(
        description="Start date and time of the event",
        example="2023-05-01T15:30:00",
    )]
    end_date_time: Annotated[datetime, Field(
        description="End date and time of the event",
        example="2023-05-01T18:30:00",
    )]
    is_display_start_date: Annotated[bool, Field(
        description="Whether to display the start date of the event",
        example=True,
    )]
    is_display_end_date: Annotated[bool, Field(
        description="Whether to display the end date of the event",
        example=True,
    )]
    time_zone: Annotated[str, Field(
        description="Time zone of the event",
        example="US/Pacific",
    )]
    event_page_language: Annotated[str, Field(
        description="Language of the event page",
        example="en-US",
    )]
