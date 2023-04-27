"""
This module defines an API for managing tickets for events using the FastAPI framework.

This module contains an APIRouter object from the FastAPI library, which handles HTTP requests to the /tickets endpoint.

Functions:
- is_valid_event_id(event_id): Determines whether the specified event ID is valid.
- is_valid_update(event_id, tickets): Updates the tickets for the specified event ID
 and returns a PlainTextResponse object indicating whether the update was successful.

Endpoints:
- POST /tickets/{event_id}: Creates tickets for the specified event ID.
- GET /tickets/{event_id}: Retrieves the tickets for the specified event ID.
- PUT /tickets/{event_id}: Updates the tickets for the specified event ID.
- DELETE /tickets/{event_id}: Deletes the tickets for the specified event ID.

"""

from typing import List
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from typing import List
from bson import ObjectId
from fastapi import APIRouter
from .db.driver import TicketDriver
from ..events.db.embeded_models.ticket import Ticket


router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)

db_handler = TicketDriver()


def is_valid_event_id(event_id):
    """
    This function determines whether the specified event ID is valid.

    Args:
    - event_id: A string representing the ID of the event.

    Returns:
    - A boolean value indicating whether the event ID is valid.
    """
    return db_handler.is_valid_event_id(event_id)


def is_valid_update(event_id, tickets):
    """
    This function updates the tickets for the specified event ID
    and returns a PlainTextResponse object indicating whether the update was successful.

    Args:
    - event_id: A string representing the ID of the event.
    - tickets: A list of Ticket objects representing the tickets to be updated.

    Returns:
    - A PlainTextResponse object indicating whether the update was successful.
    """
    if db_handler.update_tickets(event_id, tickets):
        if not tickets:
            return PlainTextResponse("Tickets deleted successfully", status_code=200)
        return PlainTextResponse("Tickets updated successfully", status_code=200)
    else:
        return PlainTextResponse("Tickets update failed", status_code=500)


@router.post(
    "/{event_id}",
    summary="Create tickets by event id",
    description="This endpoint allows you to create tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets created successfully"},
    },
)
async def create_tickets_by_event_id(event_id: str, tickets: List[Ticket]):
    """
    This endpoint creates tickets for the specified event ID.

    Args:
    - event_id: A string representing the ID of the event.
    - tickets: A list of Ticket objects representing the tickets to be created.

    Returns:
    - A PlainTextResponse object indicating whether the creation was successful.
    """
    if not is_valid_event_id(event_id):
        return PlainTextResponse("Event ID not found", status_code=404)

    tickets_in_event = db_handler.find_by_event_id(event_id)
    result = []

    tickets_as_dicts = [ticket.dict() for ticket in tickets]
    for ticket in tickets_as_dicts:
        ticket["type"] = ticket["type"].value

    result.extend(tickets_in_event["tickets"])
    result.extend(tickets_as_dicts)

    return is_valid_update(event_id, result)


@router.get(
    "/{event_id}",
    summary="Get tickets by event id",
    description="This endpoint allows you to get tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets retrieved successfully"},
    },
)
async def get_tickets_by_event_id(event_id: str) -> List[Ticket]:
    """
    This endpoint retrieves the tickets for the specified event ID.

    Args:
    - event_id: A string representing the ID of the event.

    Returns:
    - A list of Ticket objects representing the tickets for the event.
    """
    if is_valid_event_id(event_id) == 0:
        return []

    tickets = db_handler.find_by_event_id(event_id)

    result = []
    tickets = tickets["tickets"]
    for ticket in tickets:
        ticket_out = Ticket(**ticket)
        result.append(ticket_out)
    return result


@router.put(
    "/{event_id}",
    summary="Update tickets by event id",
    description="This endpoint allows you to update tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets updated successfully"},
    },
)
async def update_tickets_by_event_id(event_id: str, tickets: List[Ticket]):
    """
    This endpoint updates the tickets for the specified event ID.

    Args:
    - event_id: A string representing the ID of the event.
    - tickets: A list of Ticket objects representing the tickets to be updated.

    Returns:
    - A PlainTextResponse object indicating whether the update was successful.
    """
    if is_valid_event_id(event_id) == 0:
        return PlainTextResponse("Event not found", status_code=404)


    tickets_as_dicts = [ticket.dict() for ticket in tickets]
    for ticket in tickets_as_dicts:
        ticket["type"] = ticket["type"].value

    return is_valid_update(event_id, tickets_as_dicts)


@router.delete(
    "/{event_id}",
    summary="Delete tickets by event id",
    description="This endpoint allows you to delete tickets by event id.",
    tags=["tickets"],
    responses={
        200: {"description": "Tickets deleted successfully"},
    },
)
async def delete_tickets_by_event_id(event_id: str):
    """
    This endpoint deletes the tickets for the specified event ID.

    Args:
    - event_id: A string representing the ID of the event.

    Returns:
    - A PlainTextResponse object indicating whether the deletion was successful.
    """
    if is_valid_event_id(event_id) == 0:
        return PlainTextResponse("Event not found", status_code=404)

    return is_valid_update(event_id, [])
