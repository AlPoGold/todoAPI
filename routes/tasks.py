from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, update
from sqlalchemy import select
from slugify import slugify

from database.db_depends import get_db
from models.tasks import Task
from schemas import CreateTask

router = APIRouter(prefix='/todo', tags=['task'])


@router.get('/all_tasks')
async def get_all_categories(db: Annotated[Session, Depends(get_db)]):
    categories = db.scalars(select(Task)).all()
    return categories

@router.post('/create_task', status_code=status.HTTP_201_CREATED)
async def create_category(db: Annotated[Session, Depends(get_db)], create_task: CreateTask):
    db.execute(insert(Task).values(title=create_task.title,
                                   description=create_task.description))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }