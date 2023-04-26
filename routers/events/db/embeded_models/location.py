from enum import Enum
from typing import Annotated

from pydantic import BaseModel
from pydantic import Field


class LocationTypeEnum(str, Enum):
    venue = "venue"
    online = "online"


class Location(BaseModel):
    type: Annotated[LocationTypeEnum, Field(
        description="Type of the location (venue or online)",
        example="venue",
    )]
    location: Annotated[str | None, Field(
        description="Location string (required if type is venue)",
        example="123 Main St, San Francisco, CA 94111",
    )] = None
