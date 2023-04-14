from datetime import datetime
from pydantic import BaseModel


class State(BaseModel):
    """
    Represents the state of an event, indicating if it is public or not, and its publish date and time.

    Attributes:
        is_public (bool): Flag indicating if the event is public.
        publish_date_time (datetime): Publish date and time of the event.
    """

    is_public: bool
    publish_date_time: datetime

    class Config:
        """
        Pydantic configuration settings for State model.
        """
        schema_extra = {
            "example": {
                "is_public": True,
                "publish_date_time": "2023-04-15T14:30:00Z"
            }
        }
        orm_mode = True
