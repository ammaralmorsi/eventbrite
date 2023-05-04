from typing import Annotated,Union
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field



name_type = Annotated[str, Field(
    description="Name of the attendee",
    example="John",
)]

email_type = Annotated[str, Field(
    description="Email of the attendee",
    example="ahmed@gmail.com",
)]

reseved_ticket_type = Annotated[str, Field(
    description="Ticket type of the attendee",
    example="VIP",
)]

order_id_type = Annotated[Union[str, None], Field(
    description="Order id if ticket is added from eventbrite, none if added manually",
    example="hsjv4wgv43j3",
)]#=None #none if the ticket is added manually

event_id_type = Annotated[str, Field(
    description="Event id in db",
    example="234jhg2hf434j",
)]
class Attendees(BaseModel):
    first_name: name_type
    last_name: name_type
    email: email_type
    type_of_reseved_ticket:reseved_ticket_type
    order_id:order_id_type=None
    event_id:event_id_type

class AttendeesOut(Attendees):
        id: Annotated[str, Field(
        description="Order ID",
        example="23dfbsdbf23",
    )]
