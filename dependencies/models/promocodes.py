from typing import Annotated
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class PromoCode(BaseModel):
    name: Annotated[str, Field(
        description="Name of the promocode",
        example="SALE10",
    )]
    is_limited: Annotated[bool, Field(
        description="Flag indicating if the promocode is limited",
        example=True,
    )]
    limited_amount: Annotated[int | None, Field(
        gt=0,
        description="Limited amount of the promocode (must be greater than 0)",
        example=100,
    )] = None
    current_amount: Annotated[int | None, Field(
        gt=-1,
        description="Current amount of the promocode",
        example=100,
    )] = None
    is_percentage: Annotated[bool, Field(
        description="Flag indicating if the promocode is percentage or amount",
        example=True,
    )]
    discount_amount: Annotated[float, Field(
        gt=0,
        description="Discount percentage or amount(must be greater than 0)",
        example=0.1,
    )]
    start_date_time: Annotated[datetime, Field(
        description="Start date and time of the promocode",
        example="2023-05-01T00:00:00",
    )]
    end_date_time: Annotated[datetime, Field(
        description="End date and time of the promocode",
        example="2023-05-31T23:59:59",
    )]


class PromocodeDB(PromoCode):
    event_id: Annotated[str, Field(
        description="ID of the promocode",
        example="gshacgjhvfdks",
    )]
    id: Annotated[str, Field(
        description="ID of the promocode",
        example="gshacgjhvfdry",
    )]
