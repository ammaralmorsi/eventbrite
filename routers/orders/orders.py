from fastapi.responses import PlainTextResponse
from typing import List, Annotated
from fastapi import APIRouter, HTTPException, status, Body
from dependencies.models.orders import Order, OrderOut, OrderDB, Attendee
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
    "event_id":"event11",
    "creation_date":"2021-08-12T12:00:00.000Z",
    "price":100,
    "user_id":"ahmed55",
    "normally_ordered":True,
    "attendees":[ {
        "attendee_id":"jhsdrugksrr86e68s7d",
        "first_name":"John",
        "last_name":"Doe",
        "email":"ahmed@gmail.com",
        "type_of_reseved_ticket":"VIP",
        },
        {
        "attendee_id":"jhsdrugksrr86e6838y",
        "first_name":"Jo",
        "last_name":"Dses",
        "email":"zbc@gmail.com",
        "type_of_reseved_ticket":"REGULAR",
        }]
    })
):
    event_driver.handle_nonexistent_event(event_id)
    users_driver.handle_nonexistent_user(order.user_id)
    db_handler.add_order(event_id, order)
    return PlainTextResponse("Order added successfully.", status_code=status.HTTP_200_OK)

@router.get(
    "/order_id/{order_id}",
    summary="Get order by order id",
    description="This endpoint allows you to get order by order id.",
    responses={
        status.HTTP_200_OK : {
            "description": "Order retrieved successfully.",
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
                        "attendee_id":"jhsdrugksrr86e68s7d",
                        "first_name":"John",
                        "last_name":"Doe",
                        "email":"ahmed@gmail.com",
                        "type_of_reseved_ticket":"VIP",
                        },
                        {
                        "attendee_id":"jhsdrugksrr86e6834d",
                        "first_name":"Jo",
                        "last_name":"Dses",
                        "email":"zbc@gmail.com",
                        "type_of_reseved_ticket":"REGULAR",
                        }],
                    "tickets_count":2,
                    "id":"6454472431870302faec40c9",
                    },
        }
    }
)
async def get_order(order_id: str):
    OrderDriver.handle_nonexistent_order(order_id)
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
                    "event_id":"sadgjh232",
                    "created_date":"2021-08-12T12:00:00.000Z",
                    "price":100,
                    "user_id":"sadgjh232",
                    "normally_ordered":True,
                    "attendees":[ {
                        "attendee_id":"jhsdrugksrr86e68s7d",
                        "first_name":"John",
                        "last_name":"Doe",
                        "email":"ahmed@gmail.com",
                        "type_of_reseved_ticket":"VIP",
                        },
                        {
                        "attendee_id":"jhsdrugksrr86e68s34",
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
    users_driver.handle_nonexistent_user(user_id)
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
                        "attendee_id":"jhsdrugksrr86e68s7d",
                        "first_name":"John",
                        "last_name":"Doe",
                        "email":"ahmed@gmail.com",
                        "type_of_reseved_ticket":"VIP",
                        },
                        {
                        "attendee_id":"jhsdrugksrr86e68s34",
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
    event_driver.handle_nonexistent_event(event_id)
    return db_handler.get_event_orders(event_id)

@router.put(
    "/{order_id}/edit_order",
    summary="Edit order",
    description="This endpoint allows you to edit order.",
    responses={
        status.HTTP_200_OK: {
            "description": "Orders retrieved successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        },
    },
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

@router.get(
    "/{order_id}/get_attendees",
    summary="Get attendees",
    description="This endpoint allows you to get attendees.",
    responses={
            status.HTTP_200_OK: {
            "description": "Attendees retrieved successfully.",
            "content": {
                "attendees":[ {
                    "attendee_id":"jhsdrugksrr86e68s7d",
                    "first_name":"John",
                    "last_name":"Doe",
                    "email":"ahmed@gmail.com",
                    "type_of_reseved_ticket":"VIP",
                    },
                    {
                    "attendee_id":"jhsdrugksrr86e6838y",
                    "first_name":"Jo",
                    "last_name":"Dses",
                    "email":"zbc@gmail.com",
                    "type_of_reseved_ticket":"REGULAR",
                    }]
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        },
    },
)
async def get_attendees(order_id: str):
    db_handler.handle_nonexistent_order(order_id)
    return db_handler.get_attendees(order_id)

@router.put(
    "/{order_id}/add_attendee",
    summary="Add attendee",
    description="This endpoint allows you to add attendee.",
    responses={
        status.HTTP_200_OK:{
            "description": "Attendee added successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        }
    }
)
async def add_attendee(order_id: str ,
    attendee: Attendee=Body(..., description="Attendee object",
        example={
            "attendee_id":"jhsdrugksrr86e68s7d",
            "first_name":"John",
            "last_name":"Doe",
            "email":"ahmed@gmail.com",
            "type_of_reseved_ticket":"VIP"
            }
    )
    ):
    db_handler.handle_nonexistent_order(order_id)
    db_handler.add_attendee(order_id, attendee)
    return PlainTextResponse("Attendee added successfully.", status_code=status.HTTP_200_OK)

@router.put(
    "/{order_id}/remove_attendee/{attendee_id}",
    summary="Remove attendee",
    description="This endpoint allows you to remove attendee.",
    responses={
        status.HTTP_200_OK:{
            "description": "Attendee removed successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order or attendee not found.",
        },
    }
)
async def remove_attendee(order_id: str, attendee_id: str):
    db_handler.handle_nonexistent_order(order_id)
    db_handler.handle_nonexistent_attendee(order_id, attendee_id)
    db_handler.delete_attendee(order_id, attendee_id)
    return PlainTextResponse("Attendee removed successfully.", status_code=status.HTTP_200_OK)

@router.put(
    "/{order_id}/edit_attendee/{attendee_id}",
    summary="Edit attendee",
    description="This endpoint allows you to edit attendee but provide it by all attributes.",
    responses={
        status.HTTP_200_OK:{
            "description": "Attendee edited successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        }
    }
)
async def edit_attendee(order_id: str, attendee_id: str, updated_attributes: dict):
    db_handler.handle_nonexistent_order(order_id)
    db_handler.handle_nonexistent_attendee(order_id, attendee_id)
    db_handler.edit_attendee(order_id, attendee_id, updated_attributes)
    return PlainTextResponse("Attendee edited successfully.", status_code=status.HTTP_200_OK)
