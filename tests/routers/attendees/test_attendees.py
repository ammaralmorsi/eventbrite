from fastapi.testclient import TestClient

from main import app

from dependencies.token_handler import TokenHandler
from dependencies.models.users import UserToken
from dependencies.db.users import UsersDriver

from dependencies.db.events import EventDriver

from dependencies.db.orders import OrderDriver

user_driver = UsersDriver()
client = TestClient(app)
token_handler = TokenHandler()

