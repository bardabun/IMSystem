from fastapi import FastAPI, HTTPException, Depends
from .app import app
from typing import Callable
import logging

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    return app  # instance of FastAPI


def get_request_sender(app: FastAPI = Depends(get_app)):
    return app.state.query_inventory


@app.get("/item_amount/{item_id}")
def get_item_amount(item_id: str, query_inventory: Callable = Depends(get_request_sender)):
    logger.info(f"Processing item_id: {item_id}")
    response = query_inventory({
        "action": "get",
        "item_id": item_id,
        "attr": "amount"
    })
    logger.info(f"Response: {response}")
    if response is None:
        return {"error": "No response from query_inventory"}
    elif response['status'] == 'success':
        item_amount = response['data']
        return {"item_id": item_id, "amount": item_amount}
    else:
        logger.warning(f"Item not found: {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
