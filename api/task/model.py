from sqlalchemy import Uuid, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from database import base

task_base = base

class Task(task_base):
    __tablename__ = "task"

    id = Column(Uuid, primary_key= True, nullable= False)
    title = Column(String(30), unique= True, nullable= True)
    description = Column(String(130))
    swim_id = Column(Uuid, ForeignKey('swimlane.swim_id'))
    swimlane = relationship('SwimLane', back_populates= 'task')


