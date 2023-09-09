from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid

from .model import SwimLane

def new_swim(swim_name : str, db : Session):
    try:
        db_swim = SwimLane(
            swim_id = uuid.uuid4(),
            swim_name = swim_name
        )

        db.add(db_swim)
        db.commit()
        return{
            "swim_id" : db_swim.swim_id,
            "message" : f"swim created with the swim name {swim_name}"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR)