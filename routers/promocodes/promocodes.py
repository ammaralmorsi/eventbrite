from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from bson import ObjectId
from typing import List
from .db.driver import PromocodeDriver
from ..events.db.embeded_models.promocode import PromoCode


router = APIRouter(
    prefix="/promocodes",
    tags=["promocodes"],
)

db_handler = PromocodeDriver()


@router.post(
    "/{event_id}",
    summary="Create promocodes by event id",
    description="This endpoint allows you to create promocodes by event id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocodes created successfully"},
    },
)
async def create_promocodes_by_event_id(event_id: str, promocodes: List[PromoCode]):
    """
        Create promocodes for a given event ID.

        Args:
            event_id (str): The ID of the event to create promocodes for.
            promocodes (List[Promocode]): A list of promocodes to be created.

        Returns:
            PlainTextResponse: The response indicating whether the promocodes were created successfully or not.
        """
    promocodes_in_event = db_handler.find_by_event_id({"_id": ObjectId(event_id)})
    result = []
    result.append(promocodes_in_event)
    result.append(promocodes)

    if db_handler.update_by_event_id({"_id": ObjectId(event_id)}, {"promocodes": result}):
        return PlainTextResponse("Promocodes created successfully", status_code=201)
    else:
        return PlainTextResponse("Promocodes creation failed", status_code=500)


@router.get(
    "/{event_id}",
    summary="Get promocodes by event id",
    description="This endpoint allows you to get promocodes by event id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocodes retrieved successfully"},
    },
)
async def get_promocodes_by_event_id(event_id: str) -> List[PromoCode]:

    if db_handler.count({"_id": ObjectId(event_id)}) == 0:
        return []
    codes = db_handler.find_by_event_id({"_id": ObjectId(event_id)})
    result = []
    codes = codes["promo_codes"]
    for code in codes:
        code_out = PromoCode(**code)
        result.append(code_out)
    return result


@router.delete(
    "/{event_id}",
    summary="Delete promocodes by event id",
    description="This endpoint allows you to delete promocodes by event id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocodes deleted successfully"},
    },
)
async def delete_promocodes_by_event_id(event_id: str):
    if db_handler.delete_by_event_id({"_id": ObjectId(event_id)}):


        return PlainTextResponse("Promocodes deleted successfully", status_code=200)
    else:
        return PlainTextResponse("Promocodes deletion failed", status_code=500)
