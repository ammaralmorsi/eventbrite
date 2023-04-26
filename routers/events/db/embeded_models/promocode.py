from datetime import datetime
from pydantic import BaseModel, Field


class PromoCode(BaseModel):
    name: str = Field(..., description="Name of the promocode")
    is_limited: bool = Field(..., description="Flag indicating if the promocode is limited")
    limited_amount: int | None = Field(None, gt=0,
                                       description="Limited amount of the promocode (must be greater than 0)")
    discount_percentage: float = Field(..., gt=0, lt=1,
                                       description="Discount percentage (must be greater than 0 and less than 1)")
    start_date_time: datetime = Field(..., description="Start date and time of the promocode")
    end_date_time: datetime = Field(..., description="End date and time of the promocode")

    class Config:
        schema_extra = {
            "example": {
                "name": "SUMMER25",
                "is_limited": True,
                "limited_amount": 100,
                "discount_percentage": 0.25,
                "start_date_time": "2023-06-01T00:00:00",
                "end_date_time": "2023-09-01T23:59:59",
            }
        }
        orm_mode = True
