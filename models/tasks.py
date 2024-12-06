
from database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    date_created = Column(DateTime, default=func.now())
    completed = Column(Boolean, default=False)
    tag_id = Column(Integer, ForeignKey('tags.id'))

    tag = relationship("Tag", back_populates="tasks")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    tasks = relationship("Task", back_populates="tag")


from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))
print(CreateTable(Tag.__table__))
