from fastapi.testclient import TestClient

from main import app
from dependencies.token_handler import TokenHandler
from dependencies.models.users import UserToken
from dependencies.db.users import UsersDriver

user_driver = UsersDriver()
client = TestClient(app)
token_handler = TokenHandler()

user_signup = {
        "email": "test.test@gmail.com",
        "password": "12345",
        "firstname": "ahmed",
        "lastname": "maher"
}

user_login = {
    "username": "test.test@gmail.com",
    "password": "12345",
}

user_wrong_data = {
    "username": "test.test@gmail.com",
    "password": "12340",
}

def get_user_id(email):
    user = user_driver.get_user_by_email(email)
    return user.id

def remove_user_by_email(email):
    user_driver.collection.delete_one({"email": email})


def test_signup():
    response = client.post("/auth/signup", json=user_signup)
    assert response.status_code == 200
    assert response.text == "unverified user is created, please verify your email"


def test_signup_with_existing_email():
    response = client.post("/auth/signup", json=user_signup)
    assert response.status_code == 400
    assert response.json() == {'detail': 'email already exists'}

def test_verify_email():
    user_email = user_signup["email"]
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)
    response = client.put("/auth/verify-email", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_login():
    response = client.post("/auth/login", json=user_login)
    assert response.status_code == 422


def test_login_with_wrong_data():
    response = client.post("/auth/login", json=user_wrong_data)
    assert response.status_code == 422


def test_login_with_google():
    response = client.post("/auth/login", json=user_login)
    assert response.status_code == 422


def test_change_password_with_valid_token_and_password():
    user_email = user_signup["email"]
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)
    data = {
        "new_password": "12345"
    }
    response = client.put("/auth/change-password", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_update_password_with_valid_token_and_password():
    user_email = user_signup["email"]
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)
    data = {
        "old_password": "12345",
        "new_password": "12345"
    }
    response = client.put("/auth/update-password", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_update_password_without_valid_token_and_password():
    user_email = user_signup["email"]
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)
    token += "1"
    data = {
        "old_password": "12345",
        "new_password": "12345"
    }
    response = client.put("/auth/update-password", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    remove_user_by_email(user_signup["email"])
