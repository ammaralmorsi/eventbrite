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
    Retrieve a list of tickets for a given event ID.

    Args:
        event_id (str): The ID of the event to get tickets for.

    Returns:
        List[Ticket]: A list of tickets for the given event ID.
    """
    if db_handler.count({"_id": ObjectId(event_id)}) == 0:
        return []
    tickets = db_handler.find_by_event_id({"_id": ObjectId(event_id)})
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
async def update_tickets_by_event_id(event_id: str, tickets: List[Ticket]) -> List[Ticket]:
    """
    Update the tickets for a given event ID.

    Args:
        event_id (str): The ID of the event to update tickets for.
        tickets (List[Ticket]): The tickets to update.

    Returns:
        List[Ticket]: The updated list of tickets for the given event ID.
    """
    if db_handler.count({"_id": ObjectId(event_id)}) == 0:
        return []

    tickets_as_dicts = [ticket.dict() for ticket in tickets]
    for ticket in tickets_as_dicts:
        ticket["type"] = ticket["type"].value
    updated_tickets = db_handler.update_tickets({"_id": ObjectId(event_id)}, {"$set": {"tickets": tickets_as_dicts}})
    if updated_tickets.raw_result['n'] > 0:
        return tickets
    return []
