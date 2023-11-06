import zmq
import sys
from typing import Dict, Any

# Setup ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")  # Adjust the address and port as needed


def send_request(request) -> Dict[str, Any]:
    socket.send_json(request)
    response = socket.recv_json()
    if not isinstance(response, dict):
        print("Response recived is invalid.")
        sys.exit(1)
    print(f"Received response: {response}")
    return response
#
# Items Tests
#


def test_get_and_set():
    # Initial get request
    response = send_request(
        {"action": "get", "item_id": "item_1", "attr": "amount"})
    initial_amount = response.get('data', None)
    if initial_amount is None:
        print("Failed to get initial amount.")
        sys.exit(1)

    # Set request
    new_amount = initial_amount + 100
    response = send_request(
        {"action": "set", "item_id": "item_1", "attr": "amount", "value": new_amount})
    if response.get('status') != 'success':
        print("Failed to set new amount.")
        sys.exit(1)

    # Get request to verify the set action
    response = send_request(
        {"action": "get", "item_id": "item_1", "attr": "amount"})
    final_amount = response.get('data', None)
    if final_amount != new_amount:
        print(
            f"Failed to verify set action: expected {new_amount}, got {final_amount}")
        sys.exit(1)


def test_create_item():
    # Create request
    response = send_request({
        "action": "create",
        "item_id": "item_2",
        "name": "TestItem",
        "amount": 50,
        "price": 19.99,
        "category": "TestCategory"
    })
    if response.get('status') != 'success':
        print("Failed to create item.")
        sys.exit(1)

    # Get request to verify the create action
    response = send_request({
        "action": "get",
        "item_id": "item_2",
        "attr": "name"
    })
    item_name = response.get('data', None)
    if item_name != "TestItem":
        print(
            f"Failed to verify create action: expected TestItem, got {item_name}")
        sys.exit(1)

    print("Create item test passed.")


def test_delete_item():
    # Assuming item_2 was created in a previous test or exists in the database

    # Delete request
    response = send_request({
        "action": "delete",
        "item_id": "item_2"
    })
    if response.get('status') != 'success':
        print("Failed to delete item.")
        sys.exit(1)

    # Get request to verify the delete action
    response = send_request({
        "action": "get",
        "item_id": "item_2",
        "attr": "name"
    })
    if response.get('status') != 'error' or response.get('error') != 'Item not found':
        print("Failed to verify delete action.")
        sys.exit(1)

    print("Delete item test passed.")

    print("All items tests passed.")

#
# Sales Test
#


def test_record_sale():
    # Assuming item_1 exists and has sufficient amount
    item_id = "item_1"
    sale_quantity = 10  # Quantity to sell
    sale_price = 15.99  # Sale price per item

    # Get the initial amount of the item
    initial_response = send_request({
        "action": "get",
        "item_id": item_id,
        "attr": "amount"
    })
    initial_amount = initial_response.get('data')
    if initial_amount is None:
        print("Failed to get initial amount for the item.")
        sys.exit(1)

    # Record Sale
    response = send_request({
        "action": "sale",
        "item_id": item_id,
        "quantity": sale_quantity,
        "sale_price": sale_price
    })
    if response.get('status') != 'success':
        print("Failed to record sale.")
        sys.exit(1)
    else:
        sale_id = response.get('sale_id')
        print(f"Sale recorded with id: {sale_id}")

    # Verify inventory update
    updated_response = send_request({
        "action": "get",
        "item_id": item_id,
        "attr": "amount"
    })
    new_amount = updated_response.get('data')
    if new_amount is None or new_amount >= initial_amount:
        print(
            f"Inventory not updated after sale. Expected less than {initial_amount}, got {new_amount}")
        sys.exit(1)
    else:
        print(
            f"Inventory updated correctly after sale. New amount is {new_amount}")

    print("Record sale test passed.")


if __name__ == "__main__":
    # test_get_and_set()
    # test_create_item()
    # test_delete_item()
    test_record_sale()
