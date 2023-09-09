from fastapi import HTTPException, status
from sqlalchemy.orm import Session, aliased
import uuid
from uuid import UUID

from .model import Task
from ..swimlane.model import SwimLane

def task(swim_id : UUID, title : str, description : str, db : Session):
    try:
        db_swim_id = db.query(SwimLane.swim_id).filter(SwimLane.swim_id == swim_id).first()
        if not db_swim_id:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "no swim found, create a swim")
        
        task = db.query(Task.title).filter(title == Task.title).first()
        if task:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail= "task already exist")
        
        db_task = Task(
            id = uuid.uuid4(),
            title = title,
            description = description,
            swim_id = swim_id
        )

        db.add(db_task)
        db.commit()
        return{
            "task_id" : db_task.id,
            "message" : "task added"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
    
def move_task(task_id : UUID, to_swim_id : UUID, db : Session):
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "task not found")
        
        db_swim = db.query(SwimLane).filter(SwimLane.swim_id == to_swim_id).first()
        if not db_swim:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "swim doesn't exist")
        
        db_task.swim_id = to_swim_id
        db.commit()
        return {
            "message" : "task updated"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"an error occured{e}")
    
def show_tasks(db : Session):
    try:
        # db_tasks = db.query(Task).all()
        swim_alias = SwimLane
        db_tasks = db.query(Task.title, Task.description, swim_alias.swim_name).join(swim_alias,Task.swim_id == swim_alias.swim_id).all()
        if not db_tasks:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "no tasks found")
        return db_tasks
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
    
def get_swim_tasks(swim_id : UUID, db : Session):
    try:
        db_swim = db.query(SwimLane.swim_id).filter(SwimLane.swim_id == swim_id).first()
        if not db_swim:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= 'swim not found')
        swim_alias = aliased(SwimLane)
        db_task = db.query(Task.title, Task.description, swim_alias.swim_name).join(swim_alias,Task.swim_id == swim_alias.swim_id).filter(Task.swim_id == swim_id).all()
        if not db_task:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "tasks not found")
        # return task_details
        return db_task
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
    
def remove_task(task_id : UUID, db : Session):
    try:

        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "tasks not found")
        db.delete(db_task)
        db.commit()
        return {
            "message" : "task deleted"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
    
