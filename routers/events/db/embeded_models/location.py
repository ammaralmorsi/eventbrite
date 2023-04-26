from enum import Enum
from pydantic import BaseModel, Field


class LocationTypeEnum(str, Enum):
    venue = "venue"
    online = "online"


class Location(BaseModel):
    type: LocationTypeEnum = Field(..., description="Type of the location (venue or online)")
    location: str = Field(None, description="Location string (required if type is venue)")

    class Config:
        schema_extra = {
            "example": {
                "type": "venue",
                "location": "Example Venue Location"
            }
        }
        orm_mode = True
