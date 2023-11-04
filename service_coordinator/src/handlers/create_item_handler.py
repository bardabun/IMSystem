from fastapi import FastAPI, HTTPException, Depends, status
from .app import app
from typing import Callable
import logging

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    return app  # instance of FastAPI


def get_request_sender(app: FastAPI = Depends(get_app)):
    return app.state.query_inventory


@app.post("/create_item/{item_id}/{name}/{amount}/{price}/{category}")
def create_item(
    item_id: str,
    name: str,
    amount: int,
    price: float,
    category: str,
    query_inventory: Callable = Depends(get_request_sender)
):
    logger.info(f"Creating item: {item_id}")
    request = {
        "action": "create",
        "item_id": item_id,
        "name": name,
        "amount": amount,
        "price": price,
        "category": category
    }
    result = query_inventory(request)
    status_result = result['status']
    if status_result == "success":
        return {"status": "success"}
    else:
        error_message = result.get('error', 'Unknown error')
        logger.warning(f"Error creating {item_id}: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)
