from fastapi import HTTPException
from fastapi import status

from dependencies.db.users import UsersDriver

db = UsersDriver()


def handle_exists_email(email):
    if db.email_exists(email):
        raise HTTPException(detail="email already exists", status_code=status.HTTP_406_NOT_ACCEPTABLE)


def handle_not_exists_email(email):
    if not db.email_exists(email):
        raise HTTPException(detail="email not found", status_code=status.HTTP_404_NOT_FOUND)
