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
        return PlainTextResponse("Promocodes updated successfully", status_code=200)
    else:
        return PlainTextResponse("Promocodes update failed", status_code=500)


def is_valid_deletion(event_id, codes):
    if db_handler.update_promocodes(event_id, codes):
        return PlainTextResponse("Promocodes deleted successfully", status_code=200)
    else:
        return PlainTextResponse("Promocodes deletion failed", status_code=500)


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


@router.put(
    "/{event_id}",
    summary="Update promocodes by event id",
    description="This endpoint allows you to update promocodes by event id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocodes updated successfully"},
    },
)
async def update_promocodes_by_event_id(event_id: str, promocodes: List[PromoCode]):
    if not is_valid_event_id(event_id):
        return PlainTextResponse("Event ID is invalid", status_code=404)

    codes_as_dicts = [promocode.dict() for promocode in promocodes]

    return is_valid_update(event_id, codes_as_dicts)


@router.put(
    "/{event_id}/{name}",
    summary="Update promocode by name",
    description="This endpoint allows you to update promocode by name.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode updated successfully"},
    },
)
async def update_promocode_by_event_id_and_name(event_id: str, name: str, promocode: PromoCode):
    if not is_valid_event_id(event_id):
        return PlainTextResponse("Event ID is invalid", status_code=404)

    codes = db_handler.find_by_event_id(event_id)
    codes = codes["promo_codes"]
    codes = [code for code in codes if code["name"] != name]
    codes.append(promocode.dict())

    return is_valid_update(event_id, codes)


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


@router.get(
    "/{event_id}/{name}",
    summary="Get promocode by name",
    description="This endpoint allows you to get promocode by name.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode retrieved successfully"},
    },
)
async def get_promocode_by_event_id_and_name(event_id: str, name: str):
    if not is_valid_event_id(event_id):
        return PlainTextResponse("Event ID is invalid", status_code=404)

    codes = db_handler.find_by_event_id(event_id)
    codes = codes["promo_codes"]
    for code in codes:
        if code["name"] == name:
            code_out = PromoCode(**code)
            return code_out
    return PlainTextResponse("Promocode not found", status_code=404)


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


@router.delete(
    "/{event_id}/{name}",
    summary="Delete promocode by name",
    description="This endpoint allows you to delete promocode by name.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode deleted successfully"},
    },
)
async def delete_promocode_by_event_id_and_name(event_id: str, name: str):
    if not is_valid_event_id(event_id):
        return PlainTextResponse("Event ID is invalid", status_code=404)

    promocodes_in_event = db_handler.find_by_event_id(event_id)

    codes = []
    codes.extend(promocodes_in_event["promo_codes"])

    for code in codes:
        if code["name"] == name:
            codes.remove(code)
            break
    return is_valid_deletion(event_id, codes)


