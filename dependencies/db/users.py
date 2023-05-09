from datetime import datetime

import email_validator
from fastapi import HTTPException
from fastapi import status

from pymongo import errors as mongo_errors
from email_validator import validate_email

from dependencies.models import users
from dependencies.db.client import Client
from dependencies.utils.bson import convert_to_object_id

"""
This module contains a UsersDriver class that provides methods to interact with user data in a MongoDB database. The 
class provides methods for creating users, updating user information, verifying email addresses, and retrieving user 
information.

Functions:
    - __init__(): Initializes the class with the necessary instance variables.
    - handle_existing_email(email: str): Raises an HTTPException if the specified email already exists in the 
      database.
    - handle_nonexistent_email(email: str): Raises an HTTPException if the specified email does not exist in the 
      database.
    - handle_existing_user(user_id: str): Raises an HTTPException if a user with the specified ID already exists in 
      the database.
    - handle_nonexistent_user(user_id: str): Raises an HTTPException if a user with the specified ID does not exist 
      in the database.
    - user_exists(user_id: str) -> bool: Returns True if a user with the specified ID exists in the database, False 
      otherwise.
    - create_user(user: users.UserInSignup) -> users.UserOut: Creates a new user in the database and returns the 
      resulting user object.
    - set_is_verified(email: str): Sets the is_verified field to True for the user with the specified email address.
    - get_user_by_email(email: str) -> users.UserOut: Returns the user object for the user with the specified email 
      address.
    - email_exists(email: str): Returns True if a user with the specified email address exists in the database, False 
      otherwise.
    - update_password(email: str, password: str): Updates the password for the user with the specified email address.
    - get_user_by_id(user_id: str) -> users.UserInfo: Returns the user object for the user with the specified ID.
    - get_last_password_update_time(user_id: str) -> datetime: Returns the last time the user with the specified ID 
      updated their password.
    - edit_info(user_id, firstname, lastname, avatar): Updates the user information for the user with the specified ID.
    - validate(email): Validates the specified email address using the email_validator library.

Usage:
    Create an instance of the UsersDriver class and use its methods to interact with user data in a MongoDB database. 
    The methods can be used to create, update, and retrieve user information, as well as to verify email addresses 
    and validate email addresses.
"""

class UsersDriver:
    def __init__(self):
        self.db = Client.get_instance().get_db()
        self.collection = self.db["users"]

    def handle_existing_email(self, email: str):
        if self.email_exists(email):
            raise HTTPException(detail="email already exists", status_code=status.HTTP_400_BAD_REQUEST)

    def handle_nonexistent_email(self, email: str):
        if not self.email_exists(email):
            raise HTTPException(detail="email not found", status_code=status.HTTP_404_NOT_FOUND)

    def handle_existing_user(self, user_id: str):
        if self.user_exists(user_id):
            raise HTTPException(detail="user already exists", status_code=status.HTTP_400_BAD_REQUEST)

    def handle_nonexistent_user(self, user_id: str):
        if not self.user_exists(user_id):
            raise HTTPException(detail="user not found", status_code=status.HTTP_404_NOT_FOUND)

    def user_exists(self, user_id: str) -> bool:
        user_id = convert_to_object_id(user_id)
        return self.collection.find_one({"_id": user_id}) is not None

    def create_user(self, user: users.UserInSignup) -> users.UserOut:
        try:
            user_db = users.UserDB(last_password_update=datetime.utcnow(), **user.dict())
            inserted_id = self.collection.insert_one(user_db.dict()).inserted_id
            user_out = users.UserOut(**user_db.dict(), id=str(inserted_id))
            return user_out
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def set_is_verified(self, email: str):
        try:
            result = self.collection.update_one({"email": email}, {"$set": {"is_verified": True}})
            return result.matched_count == 1 or result.modified_count == 1
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user_by_email(self, email: str) -> users.UserOut:
        try:
            user = self.collection.find_one({"email": email})
            return users.UserOut(**user, id=str(user["_id"]))
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def email_exists(self, email: str):
        try:
            return self.collection.find_one({"email": email}) is not None
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_password(self, email: str, password: str):
        try:
            return self.collection.update_one(
                {"email": email}, {"$set": {"password": password, "last_password_update": datetime.utcnow()}}
            )
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user_by_id(self, user_id: str) -> users.UserInfo:
        self.handle_nonexistent_user(user_id)
        try:
            return users.UserInfo(id=user_id, **self.collection.find_one({"_id": convert_to_object_id(user_id)}))
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_last_password_update_time(self, user_id: str) -> datetime:
        self.handle_nonexistent_user(user_id)
        try:
            return self.collection.find_one({"_id": convert_to_object_id(user_id)})["last_password_update"]
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def edit_info(self, user_id, firstname, lastname, avatar):
        try:
            print(convert_to_object_id(user_id))
            if firstname is not None:
                self.collection.update_one({"_id": convert_to_object_id(user_id)}, {"$set": {"firstname": firstname}})
            if lastname is not None:
                self.collection.update_one({"_id": convert_to_object_id(user_id)}, {"$set": {"lastname": lastname}})
            if avatar is not None:
                self.collection.update_one({"_id": convert_to_object_id(user_id)}, {"$set": {"avatar_url": avatar}})
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def validate(self, email):
        try:
            if validate_email(email):
                pass
        except email_validator.EmailSyntaxError or email_validator.EmailNotValidError:
            raise HTTPException(detail="invalid email", status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

