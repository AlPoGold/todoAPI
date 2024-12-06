
from database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey, func
from sqlalchemy.orm import relationship

task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    date_created = Column(DateTime, default=func.now())
    completed = Column(Boolean, default=False)

    tags = relationship("Tag", secondary="task_tags", back_populates="tasks")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    tasks = relationship("Task", secondary="task_tags", back_populates="tags")


from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))
print(CreateTable(Tag.__table__))
