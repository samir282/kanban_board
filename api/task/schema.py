from pydantic import BaseModel
from uuid import UUID

class Task_Schema(BaseModel):
    title : str
    description : str

class Show_Task(BaseModel):
    title : str
    description : str
    swim_name : str