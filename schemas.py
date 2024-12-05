from datetime import datetime

from pydantic import BaseModel


class CreateTask(BaseModel):
    id: int
    title: str
    description: str = None
    date_created: datetime = datetime.now()
    completed: bool = False


