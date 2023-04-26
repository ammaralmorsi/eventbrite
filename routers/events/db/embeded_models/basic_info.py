from typing import Annotated

from pydantic import BaseModel
from pydantic import Field


class BasicInfo(BaseModel):
    title: Annotated[str, Field(
        description="Title of the event",
        example="Let's be loyal",
    )]
    organizer: Annotated[str, Field(
        description="Organizer of the event",
        example="Loyalty Organization",
    )]
    category: Annotated[str, Field(
        description="Category of the event",
        example="Loyalty",
    )]
    sub_category: Annotated[str, Field(
        description="Sub-category of the event",
        example="Loyalty",
    )]
