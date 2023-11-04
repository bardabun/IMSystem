from fastapi import FastAPI, HTTPException, Depends, status
from .app import app
from typing import Callable
import logging

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    return app  # instance of FastAPI


def get_request_sender(app: FastAPI = Depends(get_app)):
    return app.state.query_inventory


@app.delete("/delete_item/{item_id}")
def delete_item(
    item_id: str,
    query_inventory: Callable = Depends(get_request_sender)
):
    logger.info(f"Deleting item: {item_id}")
    request = {
        "action": "delete",
        "item_id": item_id
    }
    result = query_inventory(request)
    status_result = result['status']
    if status_result == "success":
        return {"status": "success"}
    else:
        error_message = result.get('error', 'Unknown error')
        logger.warning(f"Error deleting {item_id}: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)
