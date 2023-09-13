from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from .schema import Swim_Schema
from database import get_db
from .helper import new_swim, remove_swim

swim_router = APIRouter()

@swim_router.post("/create_swim", status_code= status.HTTP_201_CREATED)
def create_swim(request : Swim_Schema, db : Session = Depends(get_db)):
    print('banda logs maaghiyaa!!!!')
    return new_swim(request.swim_name, db)

@swim_router.delete("/delete_awim/{swim_id}", status_code= status.HTTP_200_OK)
async def delete_swim(swim_id : UUID, db : Session = Depends(get_db)):
    return await remove_swim(swim_id, db)

