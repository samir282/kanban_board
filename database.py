from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


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