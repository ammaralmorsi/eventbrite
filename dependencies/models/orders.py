from typing import Annotated,Optional
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
        description="Price of the order (must be greater than 0)",
        example=50,
)]

user_id_type = Annotated[str, Field(
    description="user ID(owner) in db",
    example="2dg3f4g5h6j7k8l9",
)]

tickets_count_type = Annotated[int, Field(
    description="Number of tickets in the order (must be greater than 0)",
    example=2,
)]

image_link_type = Annotated[str, Field(
    description="Image link of the event",
    example="https://www.example.com/image.png",
)]

# class OrderIn(BaseModel):#orderin
#     first_name: name_type
#     last_name: name_type
#     email: email_type
#     event_id:event_id_type
#     created_date: creation_date_type
#     price: price_type
#     image_link: image_link_type

class Order(BaseModel):#orderin
    first_name: name_type
    last_name: name_type
    email: email_type
    event_id:event_id_type
    created_date: creation_date_type
    price: price_type
    user_id: user_id_type=0
    image_link: image_link_type


class OrderOut(Order):
    id: Annotated[str, Field(
        description="Order ID",
        example="23dfbsdbf23",
    )]
    tickets_count : tickets_count_type

