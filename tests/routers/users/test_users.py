from fastapi.testclient import TestClient

from main import app
from dependencies.db.users import UsersDriver
from dependencies.token_handler import TokenHandler
from dependencies.models.users import UserToken

user_driver = UsersDriver()
token_handler = TokenHandler()
client = TestClient(app)

user_data = {
    "email": "test.test@gmail.com",
    "password": "12345",
    "firstname": "ahmed",
    "lastname": "maher"
}

user_modified_data = {
    "firstname": "ahmed",
    "lastname": "ahmed"
}

def get_token():
    user_email = user_data["email"]
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)
    return token
def get_user_id(email):
    user = user_driver.get_user_by_email(email)
    return user.id

def remove_user_by_email(email):
    user_driver.collection.delete_one({"email": email})

def test_get_info():
    token = get_token()
    response = client.get("/users/me/info", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_get_info_with_invalid_token():
    token = get_token()
    token += "1"
    response = client.get("/users/me/info", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_edit_info():
    token = get_token()
    response = client.put(
        "users/me/edit",
        data={
            "firstname": user_modified_data["firstname"],
            "lastname": user_modified_data["lastname"]
        },
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_edit_info_with_invalid_token():
    token = get_token()
    token += "1"
    response = client.put(
        "users/me/edit",
        data={
            "firstname": user_modified_data["firstname"],
            "lastname": user_modified_data["lastname"]
        },
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    remove_user_by_email(user_data["email"])
