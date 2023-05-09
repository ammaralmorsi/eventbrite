from typing import Annotated
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class TicketIn(BaseModel):
    """
    A Pydantic data model representing an input ticket, with validation rules for each field.

    Attributes:
        type (str): Type of the ticket (regular or VIP)
        name (str): Name of the ticket
        max_quantity (int): Quantity of tickets (must be greater than 0)
        price (int): Price of the ticket (must be greater than 0)
        sales_start_date_time (datetime): Sales start date and time of the ticket
        sales_end_date_time (datetime): Sales end date and time of the ticket
    """
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
    """
    A Pydantic data model representing a ticket in the database, with validation rules for each field.

    Attributes:
        event_id (str): Event ID of the ticket
        available_quantity (int): Available quantity of the ticket
    """

    event_id: Annotated[str, Field(
        description="Event ID of the ticket",
        example="23dfbsdbf23",
    )]
    available_quantity: Annotated[int, Field(
        description="Available quantity of the ticket",
        example=10,
    )]


class TicketOut(TicketDB):
    """
    A Pydantic data model representing a ticket output, with validation rules for each field.

    Attributes:
        id (str): Ticket ID
    """
    id: Annotated[str, Field(
        description="Ticket ID",
        example="23dfbsdbf23",
    )]
