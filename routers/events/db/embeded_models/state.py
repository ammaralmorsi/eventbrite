from typing import Annotated
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


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
