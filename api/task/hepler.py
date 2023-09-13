from fastapi import HTTPException, status
from sqlalchemy.orm import Session, aliased
import uuid
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from bson import Binary


from .model import Task
from ..swimlane.model import SwimLane
from database import collection
from .schema import Task_Schema

# async def task(swim_id : UUID, title : str, description : str, db : Session):
async def task(swim_id : UUID, request, db : Session):
    try:
        db_swim = db.query(SwimLane).filter(SwimLane.swim_id == swim_id).first()
        if not db_swim:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "no swim found, create a swim")
        
        task_data = request.dict()
        task_id = Binary.from_uuid(uuid.uuid4())
        task_data["task_id"] = task_id
        task_data["swim_id"] = Binary.from_uuid(db_swim.swim_id)
        task_data["swim_name"] = db_swim.swim_name

        # Insert the user data into MongoDB
        await collection.insert_one(task_data)

        # result = await collection.find_one({"title" : task_data["title"]})
        return {
            "id" : UUID(bytes= task_data["task_id"]),
            "message" : "task added"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
    
async def update_task(task_id : UUID, to_swim_id : UUID, db : Session):
    try:
        db_task = await collection.find_one({"task_id" : Binary.from_uuid(task_id)})
        if not db_task:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
        
        db_swim = db.query(SwimLane).filter(SwimLane.swim_id == to_swim_id).first()
        if not db_swim:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "swim doesn't exist")

        collection.update_one(
            {"task_id" : Binary.from_uuid(task_id)},
            {
                "$set": {"swim_id" : Binary.from_uuid(to_swim_id), "swim_name" : db_swim.swim_name}
            }    
        )
        return {
            "message" : "task updated"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"an error occured{e}")
    
async def show_tasks(db : Session):
    try:
        # db_tasks = db.query(Task).all()
        swim_alias = SwimLane
        all_tasks = await collection.find({}).to_list(length= None)
        # db_tasks = db.query(Task.title, Task.description, swim_alias.swim_name).join(swim_alias,Task.swim_id == swim_alias.swim_id).all()
        # if not db_tasks:
        #     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "no tasks found")
        # return db_tasks
        return all_tasks
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
    
async def get_swim_tasks(swim_id : UUID, db : Session):
    try:
        db_swim = db.query(SwimLane.swim_id).filter(SwimLane.swim_id == swim_id).first()
        if not db_swim:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= 'swim not found')
        
        tasks = await collection.find({"swim_id" : Binary.from_uuid(swim_id)}).to_list(length= None)
        if not tasks:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "tasks not found")
        # return task_details
        return tasks
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
    
async def remove_task(task_id : UUID):
    try:
        await collection.delete_one({"task_id" : Binary.from_uuid(task_id)})
        return {
            "message" : "task deleted"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
    
async def remove_swim_tasks(swim_id : UUID, db : Session):
    try:
        db_swim = db.query(SwimLane).filter(SwimLane.swim_id == swim_id).first()
        if not db_swim:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Swim not found")
        
        await collection.delete_many({"swim_id" : Binary.from_uuid(swim_id)})

        return {
            "mesage" : "tasks deleted"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
    
async def remove_all_tasks():
    try:
        await collection.delete_many({})
        return {
            "mesage" : "all tasks deleted"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"an error occured{e}")
