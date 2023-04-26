from typing import Annotated
from enum import Enum
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class TicketTypeEnum(str, Enum):
    regular = "regular"
    vip = "vip"


class Ticket(BaseModel):
    type: Annotated[TicketTypeEnum, Field(
        description="Type of the ticket (regular or VIP)",
        example=TicketTypeEnum.regular,
    )]
    name: Annotated[str, Field(
        description="Name of the ticket",
        example="Regular Ticket",
    )]
    quantity: Annotated[int, Field(
        gt=0,
        description="Quantity of tickets (must be greater than 0)",
        example=10,
    )]
    price: Annotated[int, Field(
        gt=0,
        description="Price of the ticket (must be greater than 0)",
        example=50,
    )]
    sales_start_date_time: Annotated[datetime, Field(
        description="Sales start date and time of the ticket",
        example="2023-05-01T00:00:00",
    )]
    sales_end_date_time: Annotated[datetime, Field(
        description="Sales end date and time of the ticket",
        example="2023-05-31T23:59:59",
    )]
