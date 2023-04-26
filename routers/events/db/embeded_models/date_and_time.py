from datetime import datetime
from pydantic import BaseModel


class DateAndTime(BaseModel):
    start_date_time: datetime
    end_date_time: datetime
    is_display_start_date: bool
    is_display_end_date: bool
    time_zone: str
    event_page_language: str

    class Config:
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
