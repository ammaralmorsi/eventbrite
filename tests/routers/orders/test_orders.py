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

correct_email="ahmedfathy1234553@gmail.com"#shoul be in users db
correct_event_id="6459447df0c9d6f57d894a60"#shoul be in  db
incorrect_event_id="6459447df0c9d6f57d813a61"
correct_order_id="645a684c256999d2fe474f81"#shoul be in users db
incorrect_order_id="64594a6ec8bd709f5481b8a9"
added_order_id=""
#correct order
order1 = {
    "first_name":"ff",
    "last_name":"Doe",
    "email":correct_email,
    "event_id":correct_event_id,
    "created_date":"2021-08-12T12:00:00.000Z",
    "price":100,
    "image_link":"https://www.f.com/image.png"
    }
#incorrect order
order2 = {
    "first_name":"John",
    "last_name":"Doe",
    "email":correct_email,
    "event_id":incorrect_event_id,
    "created_date":"2021-08-12T12:00:00.000Z",
    "price":100,
    "image_link":"https://www.example.com/image.png"
    }


def get_user_id(email):
    user = user_driver.get_user_by_email(email)
    return user.id

def test_add_order():
    user_email = order1["email"]
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)

    response = client.post("/orders/6459447df0c9d6f57d894a60/add_order", json=order1,headers={"Authorization": f"Bearer {token}"})
    added_order_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json()["first_name"] == order1["first_name"]

def test_add_order_with_wrong_event_id():
    user_email = order1["email"]
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)

    response = client.post("/orders/6459447df0c9d6f57d894a61/add_order", json=order1,headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "event not found"

def test_get_order():
    response = client.get(f"/orders/{incorrect_order_id}")
    assert response.status_code == 404

def test_get_myorders():
    user_email = correct_email
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)

    response = client.get(f"/orders/myorders",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_get_orders_by_event_id():
    response = client.get(f"/orders/event_id/{correct_event_id}")
    assert response.status_code == 200

def test_get_orders_by_event_id():
    response = client.get(f"/orders/event_id/{incorrect_event_id}")
    assert response.status_code == 404

def test_update_order():
    user_email = correct_email
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)

    response = client.put(f"/orders/{correct_order_id}/edit_order",json={"first_name":"John"},headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_update_order_with_wrong_order_id():
    user_email = correct_email
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)

    response = client.put(f"/orders/{incorrect_order_id}/edit_order",json={"first_name":"John"},headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_delete_order():
    user_email = correct_email
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)

    response = client.delete(f"/orders/{correct_order_id}/delete_order",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200