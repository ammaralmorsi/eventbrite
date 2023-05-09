from typing import Annotated
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class TicketIn(BaseModel):
    type: Annotated[str, Field(
        description="Type of the ticket (regular or VIP)",
        example="regular",
    )]
    name: Annotated[str, Field(
        description="Name of the ticket",
        example="Regular Ticket",
    )]
    max_quantity: Annotated[int, Field(
        gt=0,
        description="Quantity of tickets (must be greater than 0)",
        example=10,
    )]
    price: Annotated[int, Field(
        gt=-1,
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


class TicketDB(TicketIn):
    event_id: Annotated[str, Field(
        description="Event ID of the ticket",
        example="23dfbsdbf23",
    )]
    available_quantity: Annotated[int, Field(
        description="Available quantity of the ticket",
        example=10,
    )]


class TicketOut(TicketDB):
    id: Annotated[str, Field(
        description="Ticket ID",
        example="23dfbsdbf23",
    )]
