from fastapi import FastAPI

from api.task.model import task_base
from api.swimlane.model import swimlane_base
from database import engine
from api.routes.router import router

task_base.metadata.create_all(bind = engine)
swimlane_base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(router, prefix= "/api")