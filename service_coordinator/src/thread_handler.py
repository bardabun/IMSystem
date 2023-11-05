import zmq

context = zmq.Context()


def handle_request(request):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send_json(request)
    response = socket.recv_json()
    socket.close()  # Don't forget to close the socket when done
    return response


def thread_worker(request):
    response = handle_request(request)
    # process the response or add it to a thread-safe queue for further processing
    return response
