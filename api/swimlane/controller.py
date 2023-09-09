from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from .schema import Swim_Schema
from database import get_db
from .helper import new_swim

swim_router = APIRouter()

@swim_router.post("/create_swim", status_code= status.HTTP_201_CREATED)
def create_swim(request : Swim_Schema, db : Session = Depends(get_db)):
    print('banda logs maaghiyaa!!!!')
    return new_swim(request.swim_name, db)

