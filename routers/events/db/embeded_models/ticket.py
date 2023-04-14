from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class TicketTypeEnum(str, Enum):
    """
    Enumeration representing the types of tickets (regular or VIP).
    """

    regular = "regular"
    vip = "vip"


class Ticket(BaseModel):
    """
    Represents a ticket for an event, including its type, name, quantity, price, and sales start and end date/time.

    Attributes:
        type (TicketTypeEnum): Type of the ticket (regular or VIP).
        name (str): Name of the ticket.
        quantity (int): Quantity of tickets (must be greater than 0).
        price (int): Price of the ticket (must be greater than 0).
        sales_start_date_time (datetime): Sales start date and time of the ticket.
        sales_end_date_time (datetime): Sales end date and time of the ticket.
    """

    type: TicketTypeEnum = Field(..., description="Type of the ticket (regular or VIP)")
    name: str = Field(..., description="Name of the ticket")
    quantity: int = Field(..., gt=0, description="Quantity of tickets (must be greater than 0)")
    price: int = Field(..., gt=0, description="Price of the ticket (must be greater than 0)")
    sales_start_date_time: datetime = Field(..., description="Sales start date and time of the ticket")
    sales_end_date_time: datetime = Field(..., description="Sales end date and time of the ticket")

    class Config:
        """
        Pydantic configuration settings for Ticket model.
        """
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
