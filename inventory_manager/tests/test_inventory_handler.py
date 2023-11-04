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

    print("All tests passed.")


if __name__ == "__main__":
    test_get_and_set()
    test_create_item()  # Call the new test function
    test_delete_item()  # Call the new test function
