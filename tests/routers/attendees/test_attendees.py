from fastapi.testclient import TestClient

from main import app

from dependencies.token_handler import TokenHandler
from dependencies.models.users import UserToken
from dependencies.db.users import UsersDriver

from dependencies.db.events import EventDriver
from dependencies.db.orders import OrderDriver
from dependencies.db.attendees import AttendeeDriver

user_driver = UsersDriver()
client = TestClient(app)
token_handler = TokenHandler()

correct_email="ahmedfathy1234553@gmail.com"#should be in users db
correct_event_id="6459447df0c9d6f57d894a60"#should be in  db
incorrect_event_id="6459447df0c9d6f57d813a61"
correct_order_id="645a684c256999d2fe474f81"#should be in users db
incorrect_order_id="64594a6ec8bd709f5481b8a9"
correct_attendee_id="64598a3f3cd0d04c70730b72"
incorrect_attendee_id="64594a6ec8bd709f5481b3b3"
added_attendee_id=""

attendee1 = {
        "first_name":"John",
        "last_name":"Doe",
        "email":correct_email,
        "type_of_reseved_ticket":"VIP",
        "order_id":correct_order_id,
        "event_id":correct_event_id,
    }

def get_user_id(email):
    user = user_driver.get_user_by_email(email)
    return user.id

def test_add_attendee():
    user_email = attendee1["email"]
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)

    response = client.post("/attendees/correct_event_id/add_attendee", json=attendee1,headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400

def test_get_attendees_by_event_id():
    response = client.get("/attendees/incorrect_event_id/get_attendees")
    assert response.status_code == 400

def test_get_attendee_by_id():
    response = client.get("/attendees/incorrect_attendee_id/get_attendee")
    assert response.status_code == 400

def test_update_attendee():
    user_email = attendee1["email"]
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)

    response = client.put(f"/attendees/incorrect_attendee_id/update_attendee",json={"first_name":"sanaa"},headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400

def test_delete_attendee():
    user_email = attendee1["email"]
    user_id = get_user_id(user_email)
    user = UserToken(email=user_email, id=user_id)
    token = token_handler.encode_token(user)

    response = client.delete(f"/attendees/incorrect_attendee_id/delete_attendee",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400