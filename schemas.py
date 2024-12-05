from datetime import datetime

from pydantic import BaseModel


class CreateTask(BaseModel):
    id: int
    title: str
    description: str = None
    created_date: datetime = datetime.now()
    completed: bool = False


