import zmq
from src.handlers import app
import dotenv
import uvicorn
from logging_config import configure_logging
from setup import setup_app

setup_app()

if __name__ == "__main__":
    # Initializations
    dotenv.load_dotenv(r'..\.env')  # Updated this line

    uvicorn.run(
        app=app,
        host='127.0.0.1',
        port=8000,
    )
