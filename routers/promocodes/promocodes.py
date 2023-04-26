from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from typing import List
from .db.driver import PromocodeDriver
from ..events.db.embeded_models.promocode import PromoCode


router = APIRouter(
    prefix="/promocodes",
    tags=["promocodes"],
)

db_handler = PromocodeDriver()


def is_valid_event_id(event_id):
    return db_handler.is_valid_event_id(event_id)


def is_valid_update(event_id, codes):
    if db_handler.update_promocodes(event_id, codes):
        if not codes:
            return PlainTextResponse("Tickets deleted successfully", status_code=200)
        return PlainTextResponse("Tickets updated successfully", status_code=200)
    else:
        return PlainTextResponse("Tickets update failed", status_code=500)


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
    if not is_valid_event_id(event_id):
        return PlainTextResponse("Event ID is invalid", status_code=404)

    codes_as_dicts = [promocode.dict() for promocode in promocodes]
    promocodes_in_event = db_handler.find_by_event_id(event_id)

    result = []
    result.extend(promocodes_in_event["promo_codes"])
    result.extend(codes_as_dicts)

    return is_valid_update(event_id, result)


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

    if not is_valid_event_id(event_id):
        return []

    codes = db_handler.find_by_event_id(event_id)
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
    if not is_valid_event_id(event_id):
        return PlainTextResponse("Event ID is invalid", status_code=404)

    return is_valid_update(event_id, [])
