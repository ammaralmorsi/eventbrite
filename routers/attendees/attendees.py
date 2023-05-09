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
from dependencies.models.users import UserToken
from fastapi import Depends


router = APIRouter(
    prefix="/attendees",
    tags=["attendees"],
)

db_handler = AttendeeDriver()
users_driver = UsersDriver()
event_driver = EventDriver()
order_driver = OrderDriver()
#token
token_handler = TokenHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized.",
        },
    },
)
async def add_attendee(event_id: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    attendee: Attendee = Body(...,description="Attendee model",
    example={
        "first_name":"John",
        "last_name":"Doe",
        "email":"ahmed@gmail.com",
        "type_of_reseved_ticket":"VIP",
        "order_id":"64594a6ec8bd709f5881b8a8",
        "event_id":"6459447df0c9d6f57d894a60",
    })
    )->AttendeeOut:
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)#i think this is not needed
    event_driver.handle_nonexistent_event(event_id)
    order_driver.handle_nonexistent_order(attendee.order_id)
    #update the count of order tickets
    #order_driver.upate_tickets_count(attendee.order_id, 1)
    return db_handler.add_attendee(event_id, attendee)

@router.get(
    "/{attendee_id}/get_attendee",
    summary="Get attendee by id",
    description="This endpoint allows you to get attendee by id.",
    responses={
        status.HTTP_200_OK: {
            "description":"Attendee retrieved successfully",
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
            "description": "Attendee not found.",
        }
    }
)
async def get_attendee(attendee_id: str)->AttendeeOut:
    db_handler.handle_nonexistent_attendee(attendee_id)
    return db_handler.get_attendee(attendee_id)

@router.get(
    "/{event_id}/get_attendees",
    summary="Get attendees by event id",
    description="This endpoint allows you to get attendees by event id.",
    responses={
        status.HTTP_200_OK: {
            "description":"Attendees retrieved successfully",
            "content": [{
                "first_name":"John",
                "last_name":"Doe",
                "email":"ahmed@gmail.com",
                "type_of_reseved_ticket":"VIP",
                "order_id":"64594a6ec8bd709f5881b811",
                "event_id":"6459447df0c9d6f57d894a60",
                "id":"sadgjh232",
            },
            {
                "first_name":"hana",
                "last_name":"fahme",
                "email":"go@go.com",
                "type_of_reseved_ticket":"VIP",
                "order_id":"64594a6ec8bd709f5881b8a2",
                "event_id":"6459447df0c9d6f57d894a60",
                "id":"sadgjh2343",
            },
            {
                "first_name":"gamal",
                "last_name":"hossam",
                "email":"hi@hi.com",
                "type_of_reseved_ticket":"VIP",
                "order_id":"64594a6ec8bd709f5881b8a3",
                "event_id":"6459447df0c9d6f57d894a60",
                "id":"sadgjh235",
            }
            ]
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found.",
        },
    }
)
async def get_attendees(event_id: str)->List[AttendeeOut]:
    event_driver.handle_nonexistent_event(event_id)
    return db_handler.get_attendees(event_id)

@router.get(
    "/order/{order_id}",
    summary="Get attendees by order id",
    description="This endpoint allows you to get attendees by order id.",
    responses={
        status.HTTP_200_OK: {
            "description":"Attendees retrieved successfully",
            "content": [{
                "first_name":"John",
                "last_name":"Doe",
                "email":"ahmed@gmail.com",
                "type_of_reseved_ticket":"VIP",
                "order_id":"64594a6ec8bd709f5881b8a8",
                "event_id":"6459447df0c9d6f57d894a60",
                "id":"sadgjh232",
            },
            {
                "first_name":"asad",
                "last_name":"Doe",
                "email":"go@go.com",
                "type_of_reseved_ticket":"VIP",
                "order_id":"64594a6ec8bd709f5881b8a8",
                "event_id":"6459447df0c9d6f57d894a11",
                "id":"sadgjh2343",
            },
            {
                "first_name":"mona",
                "last_name":"Doe",
                "email":"hi@hi.com",
                "type_of_reseved_ticket":"VIP",
                "order_id":"64594a6ec8bd709f5881b8a8",
                "event_id":"6459447df0c9d6f57d894a68",
                "id":"sadgjh235",
            }
            ]
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Order not found.",
        },
    }
)
async def get_attendees_by_order_id(order_id: str)->List[AttendeeOut]:
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
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized.",
        },
    }
)
async def update_attendee(attendee_id: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    updated_attributes=Body(...,description="Attendee model",
    example={
        "first_name":"John",
        "last_name":"Doe",
        "email":"iman@yahoo.com",
        }
     )):
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)#i think this is not needed
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
async def delete_attendee(attendee_id: str,
    token: Annotated[str, Depends(oauth2_scheme)]):
    user: UserToken = token_handler.get_user(token)
    user_id = user.id
    users_driver.handle_nonexistent_user(user_id)#i think this is not needed
    db_handler.handle_nonexistent_attendee(attendee_id)
        #update the count of order tickets
    #order_driver.upate_tickets_count(attendee.order_id, -1)
    db_handler.delete_attendee(attendee_id)
    return PlainTextResponse("Attendee deleted successfully.", status_code=status.HTTP_200_OK)
