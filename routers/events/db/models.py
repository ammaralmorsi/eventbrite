from typing import List

from pydantic import BaseModel, Field

from .embeded_models.basic_info import BasicInfo
from .embeded_models.state import State
from .embeded_models.date_and_time import DateAndTime
from .embeded_models.location import Location
from .embeded_models.ticket import Ticket
from .embeded_models.promocode import PromoCode


class Event(BaseModel):
    """
    Represents an event with its details.
    """
    basic_info: BasicInfo = Field(..., description="Basic information of the event")
    image_link: str = Field(..., description="Image link of the event")
    summary: str = Field(..., description="Summary of the event")
    description: str = Field(..., description="Description of the event")
    state: State = Field(..., description="State of the event")
    date_and_time: DateAndTime = Field(..., description="Date and time details of the event")
    location: Location = Field(..., description="Location details of the event")
    tickets: List[Ticket] = Field(..., description="List of tickets available for the event")
    promo_codes: List[PromoCode] = Field(..., description="List of promo codes available for the event")

    class Config:
        """
        Configuration class for Event model.
        """
        schema_extra = {
            "example": {
                "basic_info": {
                    "title": "Example Event",
                    "organizer": "Example Organizer",
                    "category": "Example Category",
                    "sub_category": "Example Sub-category",
                    "tags": ["tag1", "tag2", "tag3"]
                },
                "image_link": "https://example.com/image.jpg",
                "summary": "This is an example event",
                "description": "This is an example event",
                "state": {
                    "is_public": True,
                    "publish_date_time": "2023-04-15T14:30:00Z"
                },
                "date_and_time": {
                    "start_date_time": "2023-04-15T10:00:00Z",
                    "end_date_time": "2023-04-15T12:00:00Z",
                    "is_display_start_date": True,
                    "is_display_end_date": True,
                    "time_zone": "UTC",
                    "event_page_language": "English"
                },
                "location": {
                    "type": "venue",
                    "location": "Example Venue"
                },
                "tickets": [
                    {
                        "type": "regular",
                        "name": "Regular Ticket",
                        "quantity": 100,
                        "price": 100,
                        "sales_start_date_time": "2021-01-01T00:00:00",
                        "sales_end_date_time": "2021-01-01T00:00:00",
                    },
                    {
                        "type": "vip",
                        "name": "VIP Ticket",
                        "quantity": 50,
                        "price": 200,
                        "sales_start_date_time": "2021-01-01T00:00:00",
                        "sales_end_date_time": "2021-01-01T00:00:00",
                    }
                ],
                "promo_codes": [
                    {
                        "name": "SUMMER25",
                        "is_limited": True,
                        "limited_amount": 100,
                        "discount_percentage": 0.25,
                        "start_date_time": "2023-06-01T00:00:00",
                        "end_date_time": "2023-09-01T23:59:59",
                    },
                    {
                        "name": "WINTER50",
                        "is_limited": False,
                        "discount_percentage": 0.5,
                        "start_date_time": "2023-12-01T00:00:00",
                        "end_date_time": "2024-03-01T23:59:59",
                    }
                ]
            }
        }
        orm_mode = True


class EventDB(Event):
    """
    Represents an event with its details in the database, including an additional ID field.
    """
    id: str | None = Field(None, description="Event ID")
