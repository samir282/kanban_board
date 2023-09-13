from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import motor.motor_asyncio as motor


db_url = "mysql://root:root@localhost:3306/kanban"

engine = create_engine(db_url)

session = sessionmaker(autocommit = False, bind= engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

base = declarative_base()

mongo_uri = "mongodb://localhost:27017"
client = motor.AsyncIOMotorClient(mongo_uri)
database = client["kanban"]
collection = database["tasks"]
