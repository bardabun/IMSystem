from sqlalchemy import DateTime, ForeignKey, create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(String, primary_key=True, index=True,
                unique=True)  # item_id in your data
    name = Column(String, index=True)  # item_name in your data
    amount = Column(Integer)
    price = Column(Float)
    category = Column(String, index=True)


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, ForeignKey('items.id'))
    quantity = Column(Integer)
    sale_price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
