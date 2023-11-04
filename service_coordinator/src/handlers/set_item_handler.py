from fastapi import FastAPI, HTTPException, status, Depends
from .app import app
from typing import Callable
import logging

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    return app  # instance of FastAPI


def get_request_sender(app: FastAPI = Depends(get_app)):
    return app.state.query_inventory


@app.post("/set_item_attribute/{item_id}/{attr}/{value}")
def set_item_attribute(item_id: str, attr: str, value: str, query_inventory: Callable = Depends(get_request_sender)):
    logger.info(f"Processing item_id: {item_id}")
    request = {
        "action": "set",
        "item_id": item_id,
        "attr": attr,
        "value": value
    }
    result = query_inventory(request)
    status_result = result['status']
    if status_result == "success":
        return {"status": "success"}
    else:
        error_message = result.get('error', 'Unknown error')
        logger.warning(f"Error processing {item_id}: {error_message}")
        http_status_code = status.HTTP_400_BAD_REQUEST
        if error_message == "Item not found":
            http_status_code = status.HTTP_404_NOT_FOUND
        elif error_message == "Attribute not found":
            http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        raise HTTPException(status_code=http_status_code, detail=error_message)
