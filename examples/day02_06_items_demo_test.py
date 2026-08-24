"""
Frozen snapshot of the tests written in Day 5 against the items demo router above.
Kept for reference only — not collected by pytest (see pyproject.toml's `testpaths`),
and not guaranteed to still pass, since app/main.py no longer mounts this router.
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_read_item():
    create_response = client.post("/items", json={"name": "Keyboard", "price": 49.99})
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == "Keyboard"
    assert "id" in created

    read_response = client.get(f"/items/{created['id']}")
    assert read_response.status_code == 200
    assert read_response.json() == created


def test_read_item_not_found():
    response = client.get("/items/999999")
    assert response.status_code == 404
