import pytest
from fastapi.testclient import TestClient
from src.handlers import app
from setup import setup_app

setup_app()

# Create a Test Client
client = TestClient(app)

# Utility function to get current item amount


def get_item_amount(item_id):
    response = client.get(f"/item_amount/{item_id}")
    assert response.status_code == 200
    return response.json()["amount"]

# Utility function to set item amount


def set_item_amount(item_id, new_amount):
    response = client.post(
        f"/set_item_attribute/{item_id}/amount/{new_amount}")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

# Utility function to create an item


def create_item(item_id, name, amount, price, category):
    response = client.post(
        f"/create_item/{item_id}/{name}/{amount}/{price}/{category}")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

# Utility function to delete an item


def delete_item(item_id):
    response = client.delete(f"/delete_item/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

# Utility function to record a sale


def record_sale(item_id, quantity, sale_price):
    post_url = f"/record_sale/{item_id}/{quantity}/{sale_price}"
    response = client.post(post_url)
    print(f"Request URL: {post_url}")  # Debugging: print the request URL
    # Debugging: print the response status code
    print(f"Response status code: {response.status_code}")

    assert response.status_code == 200
    response_data = response.json()
    assert 'status' in response_data and response_data['status'] == 'success'
    return response_data.get('sale_id')

# Tests


def test_set_and_get_item_attribute():
    item_id = "item_1"
    current_amount = get_item_amount(item_id)
    new_amount = current_amount + 100
    set_item_amount(item_id, new_amount)
    assert get_item_amount(item_id) == new_amount


def test_create_and_delete_item():
    item_id = "item_2"
    name = "TestItem"
    amount = 50
    price = 19.99
    category = "TestCategory"
    create_item(item_id, name, amount, price, category)
    delete_item(item_id)
    response = client.get(f"/item_amount/{item_id}")
    # Assuming 404 is returned when an item doesn't exist
    assert response.status_code == 404


@pytest.mark.benchmark(min_rounds=1)
def test_concurrent_performance(benchmark):
    benchmark(lambda: get_item_amount("item_1"))


def test_record_sale_process():
    item_id = "item_1"
    # Ensure item exists before proceeding
    if get_item_amount(item_id) == 404:
        create_item(item_id, "NewItem", 100, 10.00, "NewCategory")

    initial_amount = get_item_amount(item_id)
    quantity = 10
    sale_price = 16.1
    expected_new_amount = initial_amount - quantity

    sale_id = record_sale(item_id, quantity, sale_price)
    assert sale_id is not None
    assert get_item_amount(item_id) == expected_new_amount


# Main execution
if __name__ == "__main__":
    # test_set_and_get_item_attribute()
    # test_create_and_delete_item()
    test_record_sale_process()
