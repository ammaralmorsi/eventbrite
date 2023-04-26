from datetime import datetime
from pydantic import BaseModel


class State(BaseModel):
    is_public: bool
    publish_date_time: datetime

    class Config:
        schema_extra = {
            "example": {
                "is_public": True,
                "publish_date_time": "2023-04-15T14:30:00Z"
            }
        }
        orm_mode = True
