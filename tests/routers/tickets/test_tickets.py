from fastapi.testclient import TestClient
from main import app
from dependencies.db.tickets import TicketDriver

client = TestClient(app)
ticket_driver = TicketDriver()

new_ticket = {
    "type": "vip",
    "name": "test ticket",
    "price": 100,
    "max_quantity": 100,
    "sales_start_date_time": "2023-05-01T00:00:00",
    "sales_end_date_time": "2023-05-31T23:59:59",
}

updated_ticket = {
    "type": "vip",
    "name": "updated ticket",
    "price": 100,
    "max_quantity": 100,
    "sales_start_date_time": "2023-05-01T00:00:00",
    "sales_end_date_time": "2023-05-31T23:59:59",
}


def ticket_id():
    return ticket_driver.get_tickets("645a56ccb72d59a07bacfa53")[0].id


def test_create_tickets():
    response = client.post("/tickets/event_id/645a56ccb72d59a07bacfa53", json=[new_ticket])
    assert response.status_code == 200


def test_create_tickets_invalid_event_id():
    response = client.post("/tickets/event_id/645a56ccb72d59a07bacfa99", json=[new_ticket])
    assert response.status_code == 404
    assert response.json() == {'detail': 'Event not found'}


def test_get_tickets_by_event_id():
    response = client.get("/tickets/event_id/645a56ccb72d59a07bacfa53")
    assert response.status_code == 200


def test_get_tickets_by_invalid_event_id():
    response = client.get("/tickets/event_id/645a56ccb72d59a07bacfa99")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Event not found'}


def test_get_tickets_by_id():
    response = client.get(f"/tickets/ticket_id/{ticket_id()}")
    assert response.status_code == 200


def test_get_tickets_by_invalid_ticket_id():
    response = client.get("/tickets/ticket_id/645a4f6cde817f34feab5e99")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Ticket not found'}


def test_update_ticket_by_id():
    response = client.put(f"/tickets/ticket_id/{ticket_id()}", json=updated_ticket)
    assert response.status_code == 200


def test_update_ticket_by_invalid_id():
    response = client.put("/tickets/ticket_id/645a4f6cde817f34feab5e99", json=updated_ticket)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Ticket not found'}


def test_update_ticket_by_available_quantity_1():
    response = client.put(f"/tickets/ticket_id/{ticket_id()}/quantity/-5")
    assert response.status_code == 200


def test_update_ticket_by_available_quantity_2():
    response = client.put(f"/tickets/ticket_id/{ticket_id()}/quantity/5")
    assert response.status_code == 200


def test_update_ticket_by_available_quantity_invalid_id():
    response = client.put("/tickets/ticket_id/645a4f6cde817f34feab5e99/quantity/-10")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Ticket not found'}


def test_update_ticket_by_available_quantity_invalid_quantity_1():
    response = client.put(f"/tickets/ticket_id/{ticket_id()}/quantity/101")
    assert response.status_code == 400
    assert response.json() == {'detail': 'Too many tickets'}


def test_update_ticket_by_available_quantity_invalid_quantity_2():
    response = client.put(f"/tickets/ticket_id/{ticket_id()}/quantity/-101")
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough tickets available'}


def test_delete_ticket_by_id():
    response = client.delete(f"/tickets/ticket_id/{ticket_id()}")
    assert response.status_code == 200


def test_delete_ticket_by_invalid_id():
    response = client.delete("/tickets/ticket_id/645a4f6cde817f34feab5e99")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Ticket not found'}


def test_delete_tickets_by_event_id():
    response = client.delete("/tickets/event_id/645a56ccb72d59a07bacfa53")
    assert response.status_code == 200


def test_delete_tickets_by_invalid_event_id():
    response = client.delete("/tickets/event_id/645a56ccb72d59a07bacfa00")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Event not found'}
