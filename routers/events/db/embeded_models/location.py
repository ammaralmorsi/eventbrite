from enum import Enum
from pydantic import BaseModel, Field


class LocationTypeEnum(str, Enum):
    """
    Enumeration for the type of location.
    """

    venue = "venue"
    online = "online"


class Location(BaseModel):
    """
    Represents the location information of an event.

    Attributes:
        type (LocationTypeEnum): Type of the location, either 'venue' or 'online'.
        location (str): Location string (required if type is 'venue').
    """

    type: LocationTypeEnum = Field(..., description="Type of the location (venue or online)")
    location: str = Field(None, description="Location string (required if type is venue)")

    class Config:
        """
        Pydantic configuration settings for Location model.
        """
        schema_extra = {
            "example": {
                "type": "venue",
                "location": "Example Venue Location"
            }
        }
        orm_mode = True
