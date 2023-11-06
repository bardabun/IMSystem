from fastapi import FastAPI, HTTPException, Depends, status
from .app import app
from typing import Callable
import logging

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    return app  # instance of FastAPI


def get_request_sender(app: FastAPI = Depends(get_app)):
    return app.state.query_inventory


@app.post("/record_sale/{item_id}/{quantity}/{sale_price}")
def record_sale(
    item_id: str,
    quantity: int,
    sale_price: float,
    query_inventory: Callable = Depends(get_request_sender)
):
    logger.info(f"Recording sale: {item_id}")
    request = {
        "action": "sale",
        "item_id": item_id,
        "quantity": quantity,
        "sale_price": sale_price
    }
    result = query_inventory(request)
    status_result = result['status']
    if status_result == "success":
        return {"status": "success", "sale_id": result['sale_id']}
    else:
        error_message = result.get('error', 'Unknown error')
        logger.warning(f"Error recording sale for {item_id}: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)
