from db_connection import engine
from models import Base

if __name__ == "__main__":
    # Generate the SQL commands necessary to create tables for all of the models I've defined
    # Execute those commands on the database to which engine is connected
    Base.metadata.create_all(bind=engine)
