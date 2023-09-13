from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from bson import ObjectId

from database import get_db
from .schema import Task_Schema, Show_Task
from .hepler import task, show_tasks, update_task, get_swim_tasks, remove_task, remove_swim_tasks, remove_all_tasks
from typing import List


task_router = APIRouter()

@task_router.post("/create_task/{swim_id}", status_code= status.HTTP_201_CREATED)
async def create_task(swim_id : UUID, request : Task_Schema, db : Session = Depends(get_db)):
    # return task(swim_id, request.title, request.description, db)
    return await task(swim_id,request,db)

@task_router.put("/move_task", status_code= status.HTTP_202_ACCEPTED)
async def move_task(task_id : UUID, to_swim_id : UUID, db : Session = Depends(get_db)):
    return await update_task(task_id, to_swim_id, db) 

@task_router.post("/get_tasks", status_code= status.HTTP_200_OK, response_model= List[Show_Task])
async def get_tasks(db : Session = Depends(get_db)):
    return await show_tasks(db)

@task_router.post("/tasks/{swim_id}", status_code= status.HTTP_200_OK, response_model= List[Show_Task])
async def get_tasks_by_swim(swim_id : UUID, db : Session = Depends(get_db)):
    return await get_swim_tasks(swim_id,db)

@task_router.delete("/delete_task/{task_id}", status_code= status.HTTP_200_OK)
async def delete_task(task_id : UUID):
    return await remove_task(task_id)

@task_router.delete("/delete_swim_tasks/{swim_id}", status_code= status.HTTP_200_OK)
async def delete_swim_task(swim_id : UUID, db : Session = Depends(get_db)):
    return await remove_swim_tasks(swim_id, db)

@task_router.delete("/delete_all_tasks", status_code= status.HTTP_200_OK)
async def delete_swim_task():
    return await remove_all_tasks()
