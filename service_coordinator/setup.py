import zmq
from src.handlers import app

context = zmq.Context()
socket = context.socket(zmq.REQ)  # REQ socket for sending requests
# Connect to Inventory Manager Microservice
socket.connect("tcp://localhost:5555")


def query_inventory(request):
    socket.send_json(request)
    response = socket.recv_json()
    return response


def setup_app():
    app.state.query_inventory = query_inventory
