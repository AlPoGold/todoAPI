from database.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime, func
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    date_created = Column(DateTime, default=func.now())
    completed = Column(Boolean, default=False)

from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))
