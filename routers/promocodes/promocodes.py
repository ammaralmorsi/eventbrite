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
    """
        Retrieve a list of promocodes for a given event ID.
        """
    if db_handler.count({"_id": ObjectId(event_id)}) == 0:
        return []
    codes = db_handler.find_by_event_id({"_id": ObjectId(event_id)})
    result = []
    codes = codes["promo_codes"]
    for code in codes:
        code_out = PromoCode(**code)
        result.append(code_out)
    return result

    # @router.get(
    #     "/{event_id}/{promocode_id}",
    #     summary="Get promocode by event id and promocode id",
    #     description="This endpoint allows you to get promocode by event id and promocode id.",
    #     tags=["promocodes"],
    #     responses={
    #         200: {"description": "Promocode retrieved successfully"},
    #     },
    # )
    # async def get_promocode_by_event_id_and_promocode_id(event_id: str, promocode_id: str) -> PromoCode:
    #     """
    #     Retrieve a promocode for a given event ID and promocode ID.
    #     """
    #     return db_handler.find_by_event_id_and_promocode_id
    #     ({"_id": ObjectId(event_id)}, {"_id": ObjectId(promocode_id)})

    # @router.put(
    #     "/{event_id}/{promocode_id}",
    #     summary="Update promocode by event id and promocode id",
    #     description="This endpoint allows you to update promocode by event id and promocode id.",
    #     tags=["promocodes"],
    #     responses={
    #         200: {"description": "Promocode updated successfully"},
    #     },
    # )
    # async def update_promocode_by_event_id_and_promocode_id(event_id: str, promocode_id: str, promocode: PromoCode):
    #     """
    #     Update a promocode for a given event ID and promocode ID.
    #     """
    #     if db_handler.update_by_event_id_and_promocode_id
    #     ({"_id": ObjectId(event_id)}, {"_id": ObjectId(promocode_id)}, promocode):
    #         return PlainTextResponse("Promocode updated successfully", status_code=200)
    #     else:
    #         return PlainTextResponse("Promocode update failed", status_code=500)


@router.delete(
    "/{event_id}/{promocode_id}",
    summary="Delete promocode by event id and promocode id",
    description="This endpoint allows you to delete promocode by event id and promocode id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode deleted successfully"},
    },
)
async def delete_promocode_by_event_id_and_promocode_id(event_id: str, promocode_id: str):
    """
        Delete a promocode for a given event ID and promocode ID.
        """
    if db_handler.delete_by_event_id_and_promocode_id({"_id": ObjectId(event_id)}, {"_id": ObjectId(promocode_id)}):
        return PlainTextResponse("Promocode deleted successfully", status_code=200)
    else:
        return PlainTextResponse("Promocode deletion failed", status_code=500)


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
    """
    Delete a list of promocodes for a given event ID.
    """
    if db_handler.delete_by_event_id({"_id": ObjectId(event_id)}):
        return PlainTextResponse("Promocodes deleted successfully", status_code=200)
    else:
        return PlainTextResponse("Promocodes deletion failed", status_code=500)
