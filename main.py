from fastapi import FastAPI

from api.task.model import task_base
from database import engine

task_base.metadata.create_all(bind = engine)

app = FastAPI()