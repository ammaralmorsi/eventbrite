from fastapi.testclient import TestClient
from main import app
from dependencies.db.promocodes import PromocodeDriver

client = TestClient(app)
promocode_driver = PromocodeDriver()

new_promocode = {
    "name": "test promocode",
    "is_limited": True,
    "limited_amount": 100,
    "current_amount": 100,
    "is_percentage": True,
    "discount_amount": 0.2,
    "start_date_time": "2023-05-01T00:00:00",
    "end_date_time": "2023-05-31T23:59:59",
}

updated_promocode = {
    "code": "updated promocode",
    "discount": 10,
    "max_quantity": 100,
    "start_date_time": "2023-05-01T00:00:00",
    "end_date_time": "2023-05-31T23:59:59",
}


def promocode_id():
    return promocode_driver.get_promocodes("645a56ccb72d59a07bacfa53")[0].id


def test_create_promocodes():
    response = client.post("/promocodes/event_id/645a56ccb72d59a07bacfa53", json=[new_promocode])
    assert response.status_code == 200


def test_create_promocodes_invalid_event_id():
    response = client.post("/promocodes/event_id/645a56ccb72d59a07bacfa99", json=[new_promocode])
    assert response.status_code == 404
    assert response.json() == {'detail': 'Event ID is invalid'}


def test_get_promocodes_by_event_id():
    response = client.get("/promocodes/event_id/645a56ccb72d59a07bacfa53")
    assert response.status_code == 200


def test_get_promocodes_by_invalid_event_id():
    response = client.get("/promocodes/event_id/645a56ccb72d59a07bacfa99")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Event ID not found'}


def test_get_promocodes_by_id():
    response = client.get(f"/promocodes/promocode_id/{promocode_id()}")
    assert response.status_code == 200


def test_get_promocodes_by_invalid_promocode_id():
    response = client.get("/promocodes/promocode_id/645a4f6cde817f34feab5e99")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Promocode ID not found'}


def test_update_promocodes():
    response = client.put(f"/promocodes/promocode_id/{promocode_id()}", json=updated_promocode)
    assert response.status_code == 200


def test_update_promocodes_invalid_promocode_id():
    response = client.put("/promocodes/promocode_id/645a4f6cde817f34feab5e99", json=updated_promocode)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Promocode ID is invalid'}


def test_delete_promocode_by_id():
    response = client.delete(f"/promocodes/promocode_id/{promocode_id()}")
    assert response.status_code == 200


def test_delete_promocode_by_invalid_id():
    response = client.delete("/promocodes/promocode_id/645a4f6cde817f34feab5e99")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Promocode ID is invalid'}


def test_delete_promocodes_by_event_id():
    response = client.delete("/promocodes/event_id/645a56ccb72d59a07bacfa53")
    assert response.status_code == 200


def test_delete_promocodes_by_invalid_event_id():
    response = client.delete("/promocodes/event_id/645a56ccb72d59a07bacfa99")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Event ID is invalid'}
