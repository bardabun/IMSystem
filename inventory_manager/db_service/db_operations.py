import logging
from sqlalchemy.orm import Session
from .models import Item
from .db_connection import SessionLocal
from typing import Tuple

logger = logging.getLogger(__name__)


class DatabaseOperations:

    @staticmethod
    def get_item(item_id: str) -> Item:
        session = SessionLocal()
        item: Item = session.query(Item).filter(Item.id == item_id).first()
        logger.debug(f"Retrieved item from database: {item}")
        print(f"Retrieved item from database: {item}")
        session.close()
        return item

    @staticmethod
    def get_item_attribute(item_id: str, attr: str):
        session = SessionLocal()
        item: Item = session.query(Item).filter(Item.id == item_id).first()
        session.close()
        if item is not None:
            return getattr(item, attr, None)
        else:
            return None

    @staticmethod
    def create_item(item_id: str, name: str, amount: int, price: float, category: str) -> Tuple[bool, str]:
        session = SessionLocal()
        try:
            item = Item(id=item_id, name=name, amount=amount,
                        price=price, category=category)
            session.add(item)
            session.commit()
            return True, ""
        except Exception as e:
            session.rollback()  # Rollback the transaction in case of error
            return False, str(e)
        finally:
            session.close()

    @staticmethod
    def set_item_attribute(item_id: str, attr: str, value):
        session = SessionLocal()
        item: Item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            setattr(item, attr, value)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @staticmethod
    def delete_item(item_id: str):
        session = SessionLocal()
        item: Item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            session.delete(item)
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False
