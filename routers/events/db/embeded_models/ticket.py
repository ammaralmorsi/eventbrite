from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class TicketTypeEnum(str, Enum):
    regular = "regular"
    vip = "vip"


class Ticket(BaseModel):
    type: TicketTypeEnum = Field(..., description="Type of the ticket (regular or VIP)")
    name: str = Field(..., description="Name of the ticket")
    quantity: int = Field(..., gt=0, description="Quantity of tickets (must be greater than 0)")
    price: int = Field(..., gt=0, description="Price of the ticket (must be greater than 0)")
    sales_start_date_time: datetime = Field(..., description="Sales start date and time of the ticket")
    sales_end_date_time: datetime = Field(..., description="Sales end date and time of the ticket")

    class Config:
        schema_extra = {
            "example": {
                "type": "regular",
                "name": "Regular Ticket",
                "quantity": 100,
                "price": 100,
                "sales_start_date_time": "2021-01-01T00:00:00",
                "sales_end_date_time": "2021-01-01T00:00:00",
            }
        }
        orm_mode = True
