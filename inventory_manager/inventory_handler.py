import logging
from db_service import db_operations
from typing import Dict, Any
from db_service.models import Item, Sale
from sqlalchemy.orm import Session
from db_service.db_connection import SessionLocal

logger = logging.getLogger(__name__)


class RequestHandler:

    def __init__(self, db_operations):
        self.db_operations = db_operations
    #
    # Sale handlers
    #

    def handle_sale(self, request):
        item_id = request.get('item_id')
        quantity = request.get('quantity')
        sale_price = request.get('sale_price')

        with SessionLocal() as session:
            # Check inventory first before recording the sale
            item = self.db_operations.get_item(item_id)
            if item and item.amount >= quantity:
                item.amount -= quantity
                session.add(item)
                sale = self.db_operations.record_sale(
                    session, item_id, quantity, sale_price)

                # Attempt to commit the transaction
                try:
                    session.commit()  # This will commit both the sale and the item update
                    return {'status': 'success', 'sale_id': sale.id}
                except Exception as e:
                    session.rollback()  # Rollback the transaction if any error occurs
                    logger.error(f"Transaction failed: {e}")
                    return {'status': 'error', 'message': 'Transaction failed'}
            else:
                return {'status': 'error', 'message': 'Not enough inventory'}

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Handling request: {request}")
        action = request.get("action")
        if action == "sale":
            return self.handle_sale(request)
        #
        # Item handlers
        #
        item_id = request.get("item_id")
        attr = request.get("attr")
        value = request.get("value")

        logger.debug(f"Handling request: {request}")

        if action == "get":
            item: Item = self.db_operations.get_item(item_id)
            attr = request.get("attr")
            if attr is None or not isinstance(attr, str):
                return {'status': 'error', 'error': 'Invalid attribute name'}
            if item:
                return {'status': 'success', 'data': getattr(item, attr, None)}
            else:
                return {'status': 'error', 'error': 'Item not found'}

        elif action == "set":
            success = self.db_operations.set_item_attribute(
                item_id, attr, value)
            if success:
                return {'status': 'success'}
            else:
                return {'status': 'error', 'error': 'Failed to set item attribute'}

        elif action == "create":
            name = request.get("name")
            amount = request.get("amount")
            price = request.get("price")
            category = request.get("category")
            success, error = self.db_operations.create_item(
                item_id, name, amount, price, category)
            if success:
                return {'status': 'success'}
            else:
                return {'status': 'error', 'error': error}

        elif action == "delete":
            success = self.db_operations.delete_item(item_id)
            if success:
                return {'status': 'success'}
            else:
                return {'status': 'error', 'error': 'Failed to delete item'}

        else:
            return {'status': 'error', 'error': 'Invalid action'}
