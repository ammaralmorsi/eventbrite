from pymongo import MongoClient
from pydantic import BaseModel


class User(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    is_verified: bool = False

class LoginUser(BaseModel):
    email: str
    password: str


def get_db_conn():
    client = MongoClient('mongodb://localhost:27017')
    db = client['EventBrite']
    return db


