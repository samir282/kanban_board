from fastapi import APIRouter

from ..task.controller import task_router
from ..swimlane.controller import swim_router

router = APIRouter()

router.include_router(
    task_router,
    prefix= "/task",
    tags= ["Task"]
)

router.include_router(
    swim_router,
    prefix= "/swim",
    tags= ["Swimlane"]
)