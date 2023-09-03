from fastapi import APIRouter

from task.controller import task_router

router = APIRouter()

router.include_router(
    task_router,
    prefix= "/task",
    tags= ["Task"]
)