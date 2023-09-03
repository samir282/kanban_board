from sqlalchemy import Uuid, String, Column, Boolean

from database import base

task_base = base

class Task(task_base):
    __tablename__ = "task"

    id = Column(Uuid, primary_key= True, nullable= False)
    title = Column(String(30), unique= True, nullable= True)
    description = Column(String(130))
    todo = Column(Boolean)
    doing = Column(Boolean)
    done = Column(Boolean)
