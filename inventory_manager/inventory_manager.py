import time
import zmq
import logging
from inventory_handler import RequestHandler
from db_service.db_operations import DatabaseOperations

# Set up logging
logger = logging.getLogger(__name__)

# Set up the ZMQ context(- container for all the sockets in a single process) and socket
context = zmq.Context()
# REP socket for receiving requests and sending responses
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")  # Bind to the address and port

# Instantiate DatabaseOperations and RequestHandler
db_ops = DatabaseOperations()
request_handler = RequestHandler(db_ops)


def main():
    logger.info("Inventory Manager is running...")

    # Enter a loop to process incoming requests
    while True:
        try:
            # Receive a request
            request = socket.recv_json(
                flags=zmq.NOBLOCK)  # Non-blocking receive
            if request is not None:
                if not isinstance(request, dict):
                    logger.error(f"Invalid request format: {request}")
                    socket.send_json(
                        {"status": "error", "error": "Invalid request format"})
                    continue  # Skip to the next iteration of the loop

                logger.debug(f"Received request: {request}")

                # Handle the request using RequestHandler
                response = request_handler.handle_request(request)
                logger.debug(f"Sending response: {response}")

                # Send back the response
                socket.send_json(response)
            else:
                # No request received, sleep for a short time to reduce CPU usage
                time.sleep(0.1)
        except zmq.Again as e:
            # No message received, sleep for a short time to reduce CPU usage
            time.sleep(0.1)
        except KeyboardInterrupt:
            # Exit the loop if Ctrl + C is pressed
            logger.info("Interrupt received, stopping...")
            break
        except Exception as e:
            error_msg = f"Error processing request: {e}"
            logger.error(error_msg)
            socket.send_json({"status": "error", "error": error_msg})


if __name__ == "__main__":
    main()
