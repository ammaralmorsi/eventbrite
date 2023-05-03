from typing import Annotated
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from dependencies.models.tickets import TicketIn, TicketOut


class BasicInfo(BaseModel):
    title: Annotated[str, Field(
        description="Title of the event",
        example="Let's be loyal",
    )]
    organizer: Annotated[str, Field(
        description="Organizer of the event",
        example="Loyalty Organization",
    )]
    category: Annotated[str, Field(
        description="Category of the event",
        example="Loyalty",
    )]
    sub_category: Annotated[str, Field(
        description="Sub-category of the event",
        example="Loyalty",
    )]


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


class Location(BaseModel):
    is_online: Annotated[bool, Field(
        description="Type of the location (venue or online)",
        example="false",
    )] = False
    city: Annotated[str | None, Field(
        description="city as a string (required if type is venue)",
        example="San Francisco",
    )] = None


class State(BaseModel):
    is_public: Annotated[bool, Field(
            description="Flag indicating if the state is public or not.",
            example=True
        )
    ]
    publish_date_time: Annotated[datetime, Field(
            description="Date and time the state was published.",
            example="2023-05-01T09:00:00"
        )
    ]


basic_info_type = Annotated[BasicInfo, Field(
    description="Basic information of the event",
)]
image_link_type = Annotated[str, Field(
    description="Image link of the event",
    example="https://www.example.com/image.png",
)]
summary_type = Annotated[str, Field(
    description="Summary of the event",
    example="This is a summary of the event",
)]
description_type = Annotated[str, Field(
    description="Description of the event",
    example="This is a description of the event",
)]
state_type = Annotated[State, Field(
    description="State of the event",
)]
date_and_time_type = Annotated[DateAndTime, Field(
    description="Date and time details of the event",
)]
location_type = Annotated[Location, Field(
    description="Location details of the event",
)]
tickets_type = Annotated[list[TicketIn], Field(
    description="Tickets of the event",
)]
id_type = Annotated[str, Field(
    description="ID in db",
    example="2dg3f4g5h6j7k8l9",
)]
city_type = Annotated[str, Field(
    description="City of the event",
    example="San Francisco",
)]


class CreateEventIn(BaseModel):
    basic_info: basic_info_type
    image_link: image_link_type
    summary: summary_type
    description: description_type
    state: state_type
    date_and_time: date_and_time_type
    location: location_type
    tickets: tickets_type


class EventDB(BaseModel):
    creator_id: id_type
    basic_info: basic_info_type
    image_link: image_link_type
    summary: summary_type
    description: description_type
    state: state_type
    date_and_time: date_and_time_type
    location: location_type


class EventOut(EventDB):
    id: id_type
