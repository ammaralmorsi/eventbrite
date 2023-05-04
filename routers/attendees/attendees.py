from fastapi.responses import PlainTextResponse
from typing import List, Annotated
from fastapi import APIRouter, HTTPException, status, Body
from dependencies.models.attendees import Attendees, AttendeesOut
from dependencies.db.users import UsersDriver
from dependencies.db.attendees import AttendeesDriver
from dependencies.db.events import EventDriver

router = APIRouter(
    prefix="/attendees",
    tags=["attendees"],
)

db_handler = AttendeesDriver()
users_driver = UsersDriver()
event_driver = EventDriver()

@router.post(
    "/{event_id}/add_attendee",
    summary="Add attendee to event",
    description="This endpoint allows you to add attendee to event.",
    responses={
        status.HTTP_200_OK: {
            "description"="Attendee added successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found.",
        },
    },
)
async def add_attendee(event_id: str, attendee: Attendees):
    event_driver.handle_nonexistent_event(event_id)
    db_handler.add_attendee(event_id, attendee)
    return PlainTextResponse("Attendee added successfully.", status_code=status.HTTP_200_OK)

@router.get(
    "/{event_id}/get_attendees",
    summary="Get attendees by event id",
    description="This endpoint allows you to get attendees by event id.",
    responses={
        status.HTTP_200_OK: {
            "description"="Attendees retrieved successfully"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found.",
        },
    }
)
async def get_attendees(event_id: str):
    event_driver.handle_nonexistent_event(event_id)
    db_handler.get_attendees(event_id)
    return PlainTextResponse("Attendees retrieved successfully.", status_code=status.HTTP_200_OK)

@router.get(
    "/order/{order_id}",
    summary="Get attendees by order id",
    description="This endpoint allows you to get attendees by order id.",
    responses={
        status.HTTP_200_OK: {
            "description"="Attendees retrieved successfully"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        },
    }
)
async def get_attendees_by_order_id(order_id: str):
    return db_handler.get_attendees_by_order_id(order_id)