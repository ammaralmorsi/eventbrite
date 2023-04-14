from datetime import datetime
from pydantic import BaseModel


class DateAndTime(BaseModel):
    """
    Represents the date and time information of an event.

    Attributes:
        start_date_time (datetime): Start date and time of the event.
        end_date_time (datetime): End date and time of the event.
        is_display_start_date (bool): Flag indicating if the start date should be displayed.
        is_display_end_date (bool): Flag indicating if the end date should be displayed.
        time_zone (str): Time zone of the event.
        event_page_language (str): Language of the event page.
    """

    start_date_time: datetime
    end_date_time: datetime
    is_display_start_date: bool
    is_display_end_date: bool
    time_zone: str
    event_page_language: str

    class Config:
        """
        Pydantic configuration settings for DateAndTime model.
        """
        schema_extra = {
            "example": {
                "start_date_time": "2023-04-15T10:00:00Z",
                "end_date_time": "2023-04-15T12:00:00Z",
                "is_display_start_date": True,
                "is_display_end_date": True,
                "time_zone": "UTC",
                "event_page_language": "English"
            }
        }
        orm_mode = True
