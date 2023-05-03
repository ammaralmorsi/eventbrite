from typing import Annotated

from fastapi import status
from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer

from dependencies.db.events import EventDriver
from dependencies.db.likes import LikesDriver
from dependencies.db.users import UsersDriver
import dependencies.models.users as user_models
import dependencies.models.events as event_models
from dependencies.token_handler import TokenHandler

router = APIRouter(
    prefix="/events",
    tags=["events"],
)

event_driver = EventDriver()
users_driver = UsersDriver()
likes_driver = LikesDriver()
token_handler = TokenHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post(
    "/create",
    summary="Create a new event",
    responses={
        status.HTTP_200_OK: {
            "description": "event created",
            "content": {
                "creator_id": "2dg3f4g5h6j7k8l9",
                "basic_info": {
                    "title": "Let's be loyal",
                    "organizer": "Loyalty Organization",
                    "category": "Loyalty",
                    "sub_category": "Loyalty"
                },
                "image_link": "https://www.example.com/image.png",
                "summary": "This is a summary of the event",
                "description": "This is a description of the event",
                "state": {
                    "is_public": True,
                    "publish_date_time": "2023-05-01T09:00:00"
                },
                "date_and_time": {
                    "start_date_time": "2023-05-01T15:30:00",
                    "end_date_time": "2023-05-01T18:30:00",
                    "is_display_start_date": True,
                    "is_display_end_date": True,
                    "time_zone": "US/Pacific",
                    "event_page_language": "en-US"
                },
                "location": {
                    "type": "venue",
                    "location": "123 Main St, San Francisco, CA 94111"
                },
                "id": "2dg3f4g5h6j7k8l9"
            }
        },
    }
)
async def create_event(
        token: Annotated[str, Depends(oauth2_scheme)],
        event_in: event_models.CreateEventIn
) -> event_models.EventOut:
    user: user_models.UserToken = token_handler.get_user(token)

    users_driver.handle_nonexistent_user(user.id)

    return event_driver.create_new_event(event_models.EventDB(**event_in.dict(), creator_id=user.id))


@router.get(
    "/id/{event_id}",
    summary="Get an event by id",
    responses={
        status.HTTP_200_OK: {
            "description": "event found",
            "content": {
                "creator_id": "2dg3f4g5h6j7k8l9",
                "basic_info": {
                    "title": "Let's be loyal",
                    "organizer": "Loyalty Organization",
                    "category": "Loyalty",
                    "sub_category": "Loyalty"
                },
                "image_link": "https://www.example.com/image.png",
                "summary": "This is a summary of the event",
                "description": "This is a description of the event",
                "state": {
                    "is_public": True,
                    "publish_date_time": "2023-05-01T09:00:00"
                },
                "date_and_time": {
                    "start_date_time": "2023-05-01T15:30:00",
                    "end_date_time": "2023-05-01T18:30:00",
                    "is_display_start_date": True,
                    "is_display_end_date": True,
                    "time_zone": "US/Pacific",
                    "event_page_language": "en-US"
                },
                "location": {
                    "type": "venue",
                    "location": "123 Main St, San Francisco, CA 94111"
                },
                "id": "2dg3f4g5h6j7k8l9"
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "event not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "event not found"
                    }
                }
            }
        },
    }
)
async def get_event(
        event_id: str
) -> event_models.EventOut:
    return event_driver.get_event_by_id(event_id)


@router.delete(
    "/id/{event_id}",
    summary="Delete an event by id only if the token user is the creator",
    responses={
        status.HTTP_200_OK: {
            "description": "event deleted successfully",
            "content": {
                "text/plain": {
                    "example": "Event deleted successfully"
                },
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "user is not the creator",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "user is not the creator"
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "event not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "event not found"
                    }
                }
            }
        },
    }
)
async def delete_event(
        token: Annotated[str, Depends(oauth2_scheme)],
        event_id: str
) -> PlainTextResponse:
    user = token_handler.get_user(token)

    users_driver.handle_nonexistent_user(user.id)

    event: event_models.EventOut = event_driver.get_event_by_id(event_id)
    if event.creator_id != user.id:
        raise HTTPException(detail="user is not the creator", status_code=status.HTTP_401_UNAUTHORIZED)

    likes_driver.delete_likes_by_event_id(event_id)
    event_driver.delete_event_by_id(event_id)
    return PlainTextResponse("Event deleted successfully", status_code=200)
