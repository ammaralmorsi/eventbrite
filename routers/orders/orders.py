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
            "content": {
                    "first_name":"John",
                    "last_name":"Doe",
                    "email":"ahmed@gmail.com",
                    "event_id":"6459447df0c9d6f57d894a60",
                    "created_date":"2021-08-12T12:00:00.000Z",
                    "price":100,
                    "user_id":"64594543f0c9d6f57d894a68",
                    "image_link":"https://www.example.com/image.png",
                    "id":"jhv868753v5y3u74t"
                    }
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
    "event_id":"6459447df0c9d6f57d894a60",
    "created_date":"2021-08-12T12:00:00.000Z",
    "price":100,
    "user_id":"64594543f0c9d6f57d894a68",
    "image_link":"https://www.example.com/image.png"
    })
    ):
    event_driver.handle_nonexistent_event(event_id)
    users_driver.handle_nonexistent_user(order.user_id)
    return db_handler.add_order(event_id, order)

@router.get(
    "/order_id/{order_id}",
    summary="Get order by order id",
    description="This endpoint allows you to get order by order id.",
)
async def get_order(order_id: str):
    db_handler.handle_nonexistent_order(order_id)
    return db_handler.get_order(order_id)


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
                    "event_id":"6459447df0c9d6f57d894a60",
                    "created_date":"2021-08-12T12:00:00.000Z",
                    "price":100,
                    "user_id":"64594543f0c9d6f57d894a68",
                    "tickets_count":1,
                    "image_link":"https://www.example.com/image.png",
                    "id":"jhv868753v5y3u74t"
                    },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found.",
        },
    },
    }
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
            "content": {
                "application/json": {
                    "example": [
                        {
                            "first_name":"John",
                            "last_name":"Doe",
                            "email":"ahmed@gamil.com",
                            "event_id":"6459447df0c9d6f57d894a60",
                            "created_date":"2021-08-12T12:00:00.000Z",
                            "price":100,
                            "user_id":"64594543f0c9d6f57d894a68",
                            "tickets_count":1,
                            "image_link":"https://www.example.com/image.png",
                            "id":"jhv868753v5y3u74t"
                        }
                    ]
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found.",
        },
    },
)
async def get_orders_by_event_id(event_id: str):
    event_driver.handle_nonexistent_event(event_id)
    return db_handler.get_event_orders(event_id)

@router.put(
    "/{order_id}/edit_order",
    summary="Edit order",
    description="This endpoint allows you to edit order.",
    responses={
        status.HTTP_200_OK: {
            "description": "Order edited successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        },
    },
)
async def edit_order(order_id: str,
    updated_attributes=Body(...,description="Order model",
    example={
    "first_name":"John",
    "last_name":"Doe",
    "email":"ahmed2@gmail.com",
    })
    ):
    db_handler.handle_nonexistent_order(order_id)
    db_handler.edit_order(order_id, updated_attributes)
    return PlainTextResponse("Order edited successfully.", status_code=status.HTTP_200_OK)

@router.delete(
    "/{order_id}/delete_order",
    description="This endpoint allows you to delete order.",
    responses={
        status.HTTP_200_OK: {
            "description": "Order deleted successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        },
    },
)
async def delete_order(order_id: str):
    db_handler.handle_nonexistent_order(order_id)
    db_handler.delete_order(order_id)
    return PlainTextResponse("Order deleted successfully.", status_code=status.HTTP_200_OK)
