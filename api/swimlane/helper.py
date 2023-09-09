from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from uuid import UUID

from .model import SwimLane
from ..task.model import Task

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
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
    
def remove_swim(swim_id : UUID, db: Session):
    try:
        db_swim = db.query(SwimLane).filter(SwimLane.swim_id == swim_id).first()
        if not db_swim:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "swim not found")
        db_tasks = db.query(Task).filter(Task.swim_id == swim_id).all()
        if db_tasks:
            db.delete(db_tasks)
        db.delete(db_swim)
        db.commit()
        return {
            "message" : "swim deleted"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")