from sqlalchemy import Column, Uuid, String
from sqlalchemy.orm import relationship

from database import base

swimlane_base = base

class SwimLane(swimlane_base):
    __tablename__ = "swimlane"
    swim_id = Column(Uuid, primary_key= True)
    swim_name = Column(String(30))
    task = relationship('Task', back_populates= 'swimlane')