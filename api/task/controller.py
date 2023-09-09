from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from .schema import Task_Schema, Show_Task
from .hepler import task, show_tasks, move_task, get_swim_tasks, remove_task

task_router = APIRouter()

@task_router.post("/create_task/{swim_id}", status_code= status.HTTP_201_CREATED)
def create_task(swim_id : UUID, request : Task_Schema, db : Session = Depends(get_db)):
    return task(swim_id, request.title, request.description, db)

@task_router.put("/update_status", status_code= status.HTTP_202_ACCEPTED)
def update_task(task_id : UUID, to_swim_id : UUID, db : Session = Depends(get_db)):
    return move_task( task_id, to_swim_id, db) 

@task_router.post("/get_tasks", status_code= status.HTTP_200_OK, response_model= list[Show_Task])
def get_tasks(db : Session = Depends(get_db)):
    return show_tasks(db)

@task_router.post("/get_tasks/{swim_id}", status_code= status.HTTP_200_OK, response_model= list[Show_Task])
def get_tasks_by_swim(swim_id : UUID, db : Session = Depends(get_db)):
    return get_swim_tasks(swim_id,db)

@task_router.delete("/delee_task/{task_id}", status_code= status.HTTP_200_OK)
def delete_task(task_id : UUID, db : Session = Depends(get_db)):
    return remove_task(task_id, db)
