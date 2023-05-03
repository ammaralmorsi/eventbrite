from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import PlainTextResponse
from typing import List, Annotated
from dependencies.db.promocodes import PromocodeDriver
from dependencies.models.promocodes import PromoCode

router = APIRouter(
    prefix="/promocodes",
    tags=["promocodes"],
)

db_handler = PromocodeDriver()


def unlimited(promocode_id):
    code = db_handler.get_promocode_by_id(promocode_id)
    if code.is_limited is False:
        return True
    return False


def check_amount(promocode_id, amount):
    code = db_handler.get_promocode_by_id(promocode_id)
    if amount < 0:
        if code.current_amount + amount < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough promocodes available",
            )
        return True
    if amount > 0:
        if code.current_amount + amount > code.limited_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Too many Promocodes",
            )
        return True


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
    if not db_handler.is_valid_event_id(event_id):
        return PlainTextResponse("Event ID is invalid", status_code=404)

    db_handler.create_promocodes(event_id, promocodes)
    return PlainTextResponse("Promocodes created successfully", status_code=200)


@router.put(
    "promocode_id/{promocode_id}",
    summary="Update promocode by promocode id",
    description="This endpoint allows you to update promocode by promocode id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode updated successfully"},
    },
)
async def update_promocode_by_id(promocode_id: str,
                                 updated_promocode: Annotated[dict, Body(
                                     title="Promocode",
                                     description="Promocode to be updated",
                                     example={
                                         "name": "SALE10",
                                         "limited_amount": 100,
                                         "discount_percentage": 0.1,
                                         "start_date_time": "2023-05-01T00:00:00",
                                         "end_date_time": "2023-05-31T23:59:59"
                                     }
                                 )]):
    if not db_handler.is_valid_promocode_id(promocode_id):
        return PlainTextResponse("Promocode ID is invalid", status_code=404)

    if db_handler.update_promocode(promocode_id, updated_promocode):
        return PlainTextResponse("Promocode updated successfully", status_code=200)
    else:
        return PlainTextResponse("Promocode update failed", status_code=500)


@router.put(
    "/promocode_id/{promocode_id}/{amount}",
    summary="Update promocode amount by promocode id",
    description="This endpoint allows you to update promocode amount by promocode id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode amount updated successfully"},
    },
)
async def update_promocode_amount_by_id(promocode_id: str, amount: int):
    if not db_handler.is_valid_promocode_id(promocode_id):
        return PlainTextResponse("Promocode ID is invalid", status_code=404)

    if unlimited(promocode_id):
        return PlainTextResponse("Promocode is unlimited", status_code=200)

    check_amount(promocode_id, amount)
    if db_handler.update_promocode_amount(promocode_id, amount):
        return PlainTextResponse("Promocode amount updated successfully", status_code=200)
    else:
        return PlainTextResponse("Promocode amount update failed", status_code=500)


@router.get(
    "/event_id/{event_id}",
    summary="Get promocodes by event id",
    description="This endpoint allows you to get promocodes by event id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocodes retrieved successfully"},
    },
)
async def get_promocodes_by_event_id(event_id: str) -> List[PromoCode]:
    if not db_handler.is_valid_event_id(event_id):
        raise HTTPException(status_code=404, detail="Event ID not found")

    return db_handler.get_promocodes(event_id)


@router.get(
    "/promocode_id/{promocode_id}",
    summary="Get promocode by id",
    description="This endpoint allows you to get promocode by id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode retrieved successfully"},
    },
)
async def get_promocode_by_id(promocode_id: str):
    if not db_handler.is_valid_promocode_id(promocode_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promocode ID not found")

    return db_handler.get_promocode_by_id(promocode_id)


@router.delete(
    "event_id/{event_id}",
    summary="Delete promocodes by event id",
    description="This endpoint allows you to delete promocodes by event id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocodes deleted successfully"},
    },
)
async def delete_promocodes_by_event_id(event_id: str):
    if not db_handler.is_valid_event_id(event_id):
        return PlainTextResponse("Event ID is invalid", status_code=404)

    db_handler.delete_promocodes(event_id)
    return PlainTextResponse("Promocodes deleted successfully", status_code=200)


@router.delete(
    "/promocode_id/{promocode_id}",
    summary="Delete promocode by id",
    description="This endpoint allows you to delete promocode by id.",
    tags=["promocodes"],
    responses={
        200: {"description": "Promocode deleted successfully"},
    },
)
async def delete_promocode_by_id(promocode_id: str):
    if not db_handler.is_valid_promocode_id(promocode_id):
        return PlainTextResponse("Promocode ID is invalid", status_code=404)

    db_handler.delete_promocode_by_id(promocode_id)
    return PlainTextResponse("Promocode deleted successfully", status_code=200)

