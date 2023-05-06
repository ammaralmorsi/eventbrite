from typing import Annotated
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field



name_type = Annotated[str, Field(
    description="first/last Name of the attendee",
    example="John",
)]

email_type = Annotated[str, Field(
    description="Email of the attendee",
    example="ahmed@gmail.com",
)]

event_id_type = Annotated[str, Field(
    description="Event id in db",
    example="234jhg2hf434j",
)]

creation_date_type = Annotated[datetime, Field(
    description="Creation date of the order",
    example="2023-05-01T00:00:00",
)]

price_type = Annotated[int, Field(
        gt=0,
        description="Price of the order (must be greater than 0)",
        example=50,
)]

user_id_type = Annotated[str, Field(
    description="user ID(owner) in db",
    example="2dg3f4g5h6j7k8l9",
)]

tickets_count_type = Annotated[int, Field(
    gt=0,
    description="Number of tickets in the order (must be greater than 0)",
    example=2,
)]

normally_ordered_type = Annotated[bool, Field(
    description="True if the order is normally ordered, False if creator makes it",
    example=True,
)]

reseved_ticket_type = Annotated[str, Field(
    description="Ticket type of the attendee",
    example="VIP",
)]

class Attendee(BaseModel):
    attendee_id:user_id_type
    first_name: name_type
    last_name: name_type
    email: email_type
    type_of_reseved_ticket:reseved_ticket_type

Attendees_type = Annotated[list[Attendee], Field(
    description="Attendees of the order",
    example=[{
         "attendee_id":"2dg3f4g5h6j7k8l9",
         "first_name":"John",
         "last_name":"Doe",
         "email":"ahmed@gmail.com",
         "type_of_reseved_ticket":"VIP",
         },
         {
        "attendee_id":"2dg3f4g5h6j7k820",
        "first_name":"John",
        "last_name":"Doe",
         "email":"ahmed@gmail.com",
         "type_of_reseved_ticket":"VIP",
        }],
)]

class Order(BaseModel):#orderin
    first_name: name_type
    last_name: name_type
    email: email_type
    event_id:event_id_type
    creation_date: creation_date_type
    price: price_type
    user_id: user_id_type
    normally_ordered: normally_ordered_type
    attendees: Attendees_type

class OrderDB(Order):
    tickets_count: tickets_count_type=0


class OrderOut(OrderDB):
        id: Annotated[str, Field(
        description="Order ID",
        example="23dfbsdbf23",
    )]
