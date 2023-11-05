import logging
from concurrent.futures import ThreadPoolExecutor
from src.handlers import app
from src.thread_handler import thread_worker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a ThreadPoolExecutor with a fixed number of threads
executor = ThreadPoolExecutor(max_workers=10)


def query_inventory(request):
    # Submit the request to the executor
    future = executor.submit(thread_worker, request)
    try:
        # Wait for the future to complete and get the result
        # This will block until the result is ready
        response = future.result()
        logger.info(f"Response: {response}")
        return response
    except Exception as exc:
        logger.error(f"Request failed with exception: {exc}")
        # You could return an error response here, if appropriate
        return {"error": str(exc)}


def setup_app():
    app.state.query_inventory = query_inventory
