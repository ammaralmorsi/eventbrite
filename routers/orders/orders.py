from fastapi.responses import PlainTextResponse
from typing import List, Annotated
from fastapi import APIRouter, HTTPException, status, Body
from dependencies.models.orders import Order, OrderOut
from dependencies.db.users import UsersDriver
from dependencies.db.orders import OrderDriver
from dependencies.db.events import EventDriver

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

db_handler = OrderDriver()
users_driver = UsersDriver()
event_driver = EventDriver()


@router.post(
    "/{event_id}/add_order",
    summary="Add order to event",
    description="This endpoint allows you to add order to event.",
    responses={
        status.HTTP_200_OK: {
            "description": "Order added successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found.",
        },
    },
)
async def add_order(event_id: str,
    order: Order = Body(...,description="Order model",
    example={
    "first_name":"John",
    "last_name":"Doe",
    "email":"ahmed@gmail.com",
    "event_id":"sadgjh232",
    "creation_date":"2021-08-12T12:00:00.000Z",
    "price":100,
    "user_id":"sadgjh232",
    "normally_ordered":True,
    "attendees":[ {
        "first_name":"John",
        "last_name":"Doe",
        "email":"ahmed@gmail.com",
        "type_of_reseved_ticket":"VIP",
        },
        {
        "first_name":"Jo",
        "last_name":"Dses",
        "email":"zbc@gmail.com",
        "type_of_reseved_ticket":"REGULAR",
        }]
    })
):
    event_driver.handle_nonexistent_event(event_id)
    db_handler.add_order(event_id, order)
    return PlainTextResponse("Order added successfully.", status_code=status.HTTP_200_OK)

@router.get(
    "/user_id/{user_id}",
    summary="Get orders by user id",
    description="This endpoint allows you to get orders by user id.",
    responses={
        status.HTTP_200_OK: {
            "description": "Orders retrieved successfully.",
            "content": {
                    "first_name":"John",
                    "last_name":"Doe",
                    "email":"ahmed@gmail.com",
                    "event_id":"sadgjh232",
                    "created_date":"2021-08-12T12:00:00.000Z",
                    "price":100,
                    "user_id":"sadgjh232",
                    "normally_ordered":True,
                    "attendees":[ {
                        "first_name":"John",
                        "last_name":"Doe",
                        "email":"ahmed@gmail.com",
                        "type_of_reseved_ticket":"VIP",
                        },
                        {
                        "first_name":"Jo",
                        "last_name":"Dses",
                        "email":"zbc@gmail.com",
                        "type_of_reseved_ticket":"REGULAR",
                        }],
                    "tickets_count":2,
                    "id":"6454472431870302faec40c9",
                    },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found.",
        },
    },
    }
)
async def get_orders_by_user_id(user_id: str):
    #users_driver.handle_nonexistent_user(user_id)
    return db_handler.get_user_orders(user_id)


@router.get(
    "/event_id/{event_id}",
    summary="Get orders by event id",
    description="This endpoint allows you to get orders by event id.",
    responses={
        status.HTTP_200_OK: {
            "description": "Orders retrieved successfully.",
            "content": {
                    "first_name":"John",
                    "last_name":"Doe",
                    "email":"ahmed@gmail.com",
                    "event_id":"sadgjh232",
                    "created_date":"2021-08-12T12:00:00.000Z",
                    "price":100,
                    "user_id":"sadgjh232",
                    "normally_ordered":True,
                    "attendees":[ {
                        "first_name":"John",
                        "last_name":"Doe",
                        "email":"ahmed@gmail.com",
                        "type_of_reseved_ticket":"VIP",
                        },
                        {
                        "first_name":"Jo",
                        "last_name":"Dses",
                        "email":"zbc@gmail.com",
                        "type_of_reseved_ticket":"REGULAR",
                        }],
                    "tickets_count":2,
                    "id":"6454472431870302faec40c9",
                    },
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found.",
        },
    },
    },
)
async def get_orders_by_event_id(event_id: str):
    #event_driver.handle_nonexistent_event(event_id)
    return db_handler.get_event_orders(event_id)

@router.put(
    "/{order_id}/edit_order",
    summary="Edit order",
    description="This endpoint allows you to edit order.",
    responses={
        status.HTTP_200_OK: {
            "description": "Orders retrieved successfully.",
            "content": {
                    "first_name":"joo",
                    "price":300,
                    },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        },
    },
    }
)
async def edit_order(order_id: str,updated_attributes: dict):
    db_handler.handle_nonexistent_order(order_id)
    db_handler.edit_order(order_id, updated_attributes)
    return PlainTextResponse("Order edited successfully.", status_code=status.HTTP_200_OK)

@router.delete(
    "/{order_id}/delete_order",
    summary="Delete order",
    description="This endpoint allows you to delete order.",
    responses={
        status.HTTP_200_OK:{
            "description": "Order deleted successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        }
    }
)
async def delete_order(order_id: str):
    db_handler.handle_nonexistent_order(order_id)
    db_handler.delete_order(order_id)
    return PlainTextResponse("Order deleted successfully.", status_code=status.HTTP_200_OK)