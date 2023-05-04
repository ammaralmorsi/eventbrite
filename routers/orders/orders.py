from fastapi.responses import PlainTextResponse
from typing import List, Annotated
from fastapi import APIRouter, HTTPException, status, Body
from dependencies.models.orders import Order, OrderOut
from dependencies.db.users import UsersDriver
from dependencies.db.tickets import OrderDriver
from dependencies.db.events import EventDriver

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

db_handler = OrderDriver()
users_driver = UsersDriver()
event_driver = EventDriver()

@router.get(
    "/user_id/{user_id}",
    summary="Get orders by user id",
    description="This endpoint allows you to get orders by user id.",
    responses={
        status.HTTP_200_OK: {
            "model": List[OrderOut],#i neeed to change this with example of order
            "description": "Orders retrieved successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found.",
        },
    },
)
async def get_orders_by_user_id(user_id: str):
    users_driver.handle_nonexistent_user(user_id)
    return db_handler.get_user_orders(user_id)


@router.get(
    "/event_id/{event_id}",
    summary="Get orders by event id",
    description="This endpoint allows you to get orders by event id.",
    responses={
        status.HTTP_200_OK: {
            "model": List[OrderOut],
            "description": "Orders retrieved successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found.",
        },
    },
)
async def get_orders_by_event_id(event_id: str):
    event_driver.handle_nonexistent_event(event_id)
    return db_handler.get_event_orders(event_id)