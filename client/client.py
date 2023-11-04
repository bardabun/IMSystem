import requests


def get_item_amount(item_id):
    response = requests.get(
        f'http://127.0.0.1:8000/item_amount/{item_id}')
    if response.status_code == 200:
        return response.json()['amount_left']
    else:
        print(f'Error: {response.json()["detail"]}')


def set_item_attribute(item_id, attr, value):
    response = requests.post(
        f'http://127.0.0.1:8000/set_item_attribute/{item_id}/{attr}/{value}')
    if response.status_code == 200:
        print('Update successful')
    else:
        error_detail = response.json().get('detail', 'Unknown error')
        print(f'Error: {error_detail}')


def user_input():
    while True:
        user_command = input("Enter command (get, set, quit): ").lower()
        if user_command == 'get':
            item_id = input("Enter item ID: ")
            item_amount = get_item_amount(item_id)
            if item_amount is not None:
                print(f'Amount left of item {item_id}: {item_amount}')
        elif user_command == 'set':
            item_id = input("Enter item ID: ")
            attr = input("Enter attribute: ")
            value = input("Enter value: ")
            set_item_attribute(item_id, attr, value)
        elif user_command == 'quit':
            break
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    user_input()
