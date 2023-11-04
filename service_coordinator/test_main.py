import pytest
from fastapi.testclient import TestClient
from src.handlers import app
from setup import setup_app

setup_app()

# Create a Test Client
client = TestClient(app)


# Test set and get
def test_set_item_attribute():
    # First, get the current amount
    response = client.get("/item_amount/item_1")
    assert response.status_code == 200
    current_amount = response.json()["amount_left"]

    # Now, update the amount
    new_amount = current_amount + 100
    response = client.post(f"/set_item_attribute/item_1/amount/{new_amount}")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # Verify the updated amount
    response = client.get("/item_amount/item_1")
    assert response.status_code == 200
    assert response.json() == {"item_id": "item_1", "amount_left": new_amount}


def test_create_item():
    response = client.post(
        "/create_item/item_2/TestItem/50/19.99/TestCategory")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


def test_delete_item():
    # Assuming item_2 was created in a previous test or exists in the database
    response = client.delete("/delete_item/item_2")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # Optional: check that the item was actually deleted
    response = client.get("/item_amount/item_2")
    # Assuming 404 is returned when an item doesn't exist
    assert response.status_code == 404
