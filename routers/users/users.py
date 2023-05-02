from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer

from dependencies.db.users import UsersDriver
from dependencies.db.events import EventsDriver
from dependencies.models import users
from dependencies.models import likes
from dependencies.utils.users import handle_not_exists_email
from dependencies.token_handler import TokenHandler

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

db = UsersDriver()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
token_handler = TokenHandler()

event_driver = EventsDriver()

def get_user_info(user_id: str) -> users.UserInfo:
    db_user = db.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(detail="user not found", status_code=status.HTTP_404_NOT_FOUND)
    return users.UserInfo(**db_user)


@router.get(
    "/emails/check",
    summary="check if email is available",
    description="check if email is available",
    response_class=PlainTextResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "email is available",
            "content": {
                "text/plain": {
                    "example": "email is available"
                },
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "email not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "email not found"
                    }
                }
            }
        }
    }
)
async def check_email(email: str):
    handle_not_exists_email(email)

    return PlainTextResponse("email is available", status_code=status.HTTP_200_OK)


@router.get(
    "/info/avatar",
    summary="get the the avatar of the email sent whether it is verified or not",
    responses={
        status.HTTP_200_OK: {
            "description": "login successfully",
            "content": {
                "application/json": {
                    "example": {
                        "avatar_url": "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?s=200",
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "wrong password or email is not verified",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "wrong email",
                    }
                }
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "email not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "email not found"
                        }
                    }
                }
            }
        }
    }
)
async def get_avatar(email: str) -> users.UserAvatar:
    handle_not_exists_email(email)
    return users.UserAvatar(**db.get_user_by_email(email).dict())


@router.get(
    "/info/id/{user_id}",
    summary="get user information by id",
    description="get user information by id",
    responses={
        status.HTTP_200_OK: {
            "description": "get user information by id successfully",
            "content": {
                "application/json": {
                    "example": {
                        "email": "user@gmail.com",
                        "firstname": "user",
                        "lastname": "user",
                        "avatar_url": "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?s=200",
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "user not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "user not found"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "invalid user id",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid user id"
                    }
                }
            }
        }
    }
)
async def get_user_by_id(user_id) -> users.UserInfo:
    return get_user_info(user_id)


@router.get(
    "/info/me",
    summary="get user information",
    description="get the user firstname, lastname and avatar",
)
async def get_info(token: Annotated[str, Depends(oauth2_scheme)]) -> users.UserInfo:
    user = token_handler.get_user(token)
    return get_user_info(user.id)


@router.post(
    "/events/{event_id}/like",
    summary="like an event",
    description="like an event",
    responses={
        status.HTTP_200_OK: {
            "description": "event liked",
            "content": {
                "text/plain": {
                    "example": "event liked"
                },
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
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid toked"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "event is already liked",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "event is already liked"
                    }
                }
            }
        }
    }
)
async def like_event(event_id:str , token: Annotated[str, Depends(oauth2_scheme)]):
    user = token_handler.get_user(token)
    event_driver.get_event_by_id(event_id) 
    like_db = likes.LikeDB(event_id=event_id, user_id=user.id)
    if db.is_event_liked(like_db) :
        raise HTTPException(detail="event is already liked", status_code=status.HTTP_400_BAD_REQUEST) #check if event exists
    db.like_event(like_db)
    return PlainTextResponse("event liked", status_code=status.HTTP_200_OK)

@router.delete(
    "/events/{event_id}/unlike",
    summary="unlike an event",
    description="unlike an event",
    responses={
        status.HTTP_200_OK: {
            "description": "event unliked",
            "content": {
                "text/plain": {
                    "example": "event unliked"
                },
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
        status.HTTP_401_UNAUTHORIZED: {
            "description": "invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid toked"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "event is not liked",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "event is not liked"
                    }
                }
            }
        }
    }
)
async def unlike_event(event_id:str , token: Annotated[str, Depends(oauth2_scheme)]):
    user = token_handler.get_user(token)
    event_driver.get_event_by_id(event_id)
    like_db = likes.LikeDB(event_id=event_id, user_id=user.id)
    if not db.is_event_liked(like_db) :
        raise HTTPException(detail="event is not liked", status_code=status.HTTP_400_BAD_REQUEST)
    db.unlike_event(like_db)
    return PlainTextResponse("event unliked", status_code=status.HTTP_200_OK)
