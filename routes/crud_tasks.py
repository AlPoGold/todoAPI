from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, update, delete
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
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask):
    db.execute(insert(Task).values(title=create_task.title,
                                   description=create_task.description,
                                   date_created=create_task.date_created,
                                   completed=create_task.completed))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }
@router.put('/complete_task')
async def complete_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: CreateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no task found'
        )

    db.execute(update(Task).where(Task.id == task_id).values(completed=True))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task completing is successful'
    }


@router.put('/update_task')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: CreateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no task found'
        )

    db.execute(update(Task).where(Task.id == task_id).values(
            title=update_task.title,
            description=update_task.description,
            completed=update_task.completed))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful'
    }


@router.delete('/delete_task', status_code=status.HTTP_200_OK)
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))


    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no task found'
        )

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category task is successful'
    }
