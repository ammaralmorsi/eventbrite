from fastapi.responses import PlainTextResponse
from typing import List, Annotated
from fastapi import APIRouter, HTTPException, status, Body
from dependencies.models.attendees import Attendee, AttendeeOut
from dependencies.db.users import UsersDriver
from dependencies.db.attendees import AttendeeDriver
from dependencies.db.events import EventDriver
from dependencies.db.orders import OrderDriver
#token
from dependencies.token_handler import TokenHandler
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends


router = APIRouter(
    prefix="/attendees",
    tags=["attendees"],
)

db_handler = AttendeeDriver()
users_driver = UsersDriver()
event_driver = EventDriver()
order_driver = OrderDriver()

@router.post(
    "/{event_id}/add_attendee",
    summary="Add attendee to event",
    description="This endpoint allows you to add attendee to event.",
    responses={
        status.HTTP_200_OK: {
            "description":"Attendee added successfully.",
            "content": {
                "first_name":"John",
                "last_name":"Doe",
                "email":"ahmed@gmail.com",
                "type_of_reseved_ticket":"VIP",
                "order_id":"64594a6ec8bd709f5881b8a8",
                "event_id":"6459447df0c9d6f57d894a60",
                "id":"sadgjh232",
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found.",
        },
    },
)
async def add_attendee(event_id: str,
    attendee: Attendee = Body(...,description="Attendee model",
    example={
        "first_name":"John",
        "last_name":"Doe",
        "email":"ahmed@gmail.com",
        "type_of_reseved_ticket":"VIP",
        "order_id":"64594a6ec8bd709f5881b8a8",
        "event_id":"6459447df0c9d6f57d894a60",
    })
    ):
    event_driver.handle_nonexistent_event(event_id)
    order_driver.handle_nonexistent_order(attendee.order_id)
    #update the count of order tickets
    #order_driver.upate_tickets_count(attendee.order_id, 1)
    return db_handler.add_attendee(event_id, attendee)

@router.get(
    "/{event_id}/get_attendees",
    summary="Get attendees by event id",
    description="This endpoint allows you to get attendees by event id.",
    responses={
        status.HTTP_200_OK: {
            "description":"Attendees retrieved successfully",
            "content": {
                "first_name":"John",
                "last_name":"Doe",
                "email":"ahmed@gmail.com",
                "type_of_reseved_ticket":"VIP",
                "order_id":"64594a6ec8bd709f5881b8a8",
                "event_id":"6459447df0c9d6f57d894a60",
                "id":"sadgjh232",
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found.",
        },
    }
)
async def get_attendees(event_id: str):
    event_driver.handle_nonexistent_event(event_id)
    return db_handler.get_attendees(event_id)

@router.get(
    "/order/{order_id}",
    summary="Get attendees by order id",
    description="This endpoint allows you to get attendees by order id.",
    responses={
        status.HTTP_200_OK: {
            "description":"Attendees retrieved successfully",
            "content": {
                "first_name":"John",
                "last_name":"Doe",
                "email":"ahmed@gmail.com",
                "type_of_reseved_ticket":"VIP",
                "order_id":"64594a6ec8bd709f5881b8a8",
                "event_id":"6459447df0c9d6f57d894a60",
                "id":"sadgjh232",
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        },
    }
)
async def get_attendees_by_order_id(order_id: str):
    order_driver.handle_nonexistent_order(order_id)
    return db_handler.get_attendees_by_order_id(order_id)

@router.put(
    "/{attendee_id}/update_attendee",
    summary="Update attendee",
    description="This endpoint allows you to update attendee.",
    responses={
        status.HTTP_200_OK: {
            "description":"Attendee updated successfully"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Attendee not found.",
        },
    }
)
async def update_attendee(attendee_id: str,updated_attributes=Body(...,description="Attendee model" )):
    db_handler.handle_nonexistent_attendee(attendee_id)
    db_handler.update_attendee(attendee_id, updated_attributes)
    return PlainTextResponse("Attendee updated successfully.", status_code=status.HTTP_200_OK)

@router.delete(
    "/{attendee_id}/delete_attendee",
    summary="Delete attendee",
    description="This endpoint allows you to delete attendee.",
    responses={
        status.HTTP_200_OK: {
            "description":"Attendee deleted successfully"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Attendee not found.",
        },
    }
)
async def delete_attendee(attendee_id: str):
    db_handler.handle_nonexistent_attendee(attendee_id)
        #update the count of order tickets
    #order_driver.upate_tickets_count(attendee.order_id, -1)
    db_handler.delete_attendee(attendee_id)
    return PlainTextResponse("Attendee deleted successfully.", status_code=status.HTTP_200_OK)