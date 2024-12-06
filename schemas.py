from datetime import datetime
from typing import List

from pydantic import BaseModel


class CreateTask(BaseModel):
    id: int
    title: str
    description: str = None
    date_created: datetime = datetime.now()
    completed: bool = False

    class Config:
        orm_mode = True

class PaginatedResponse(BaseModel):
    page: int
    page_size: int
    total: int
    tasks: List[CreateTask]
