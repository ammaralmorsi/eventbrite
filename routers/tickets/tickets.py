from typing import List
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from .db.driver import TicketDriver
from ..events.db.embeded_models.ticket import Ticket

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)

db_handler = TicketDriver()


def is_valid_event_id(event_id):
    return db_handler.is_valid_event_id(event_id)


def is_valid_update(event_id, tickets):
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

    if is_valid_event_id(event_id) == 0:
        return PlainTextResponse("Event not found", status_code=404)

    return is_valid_update(event_id, [])
