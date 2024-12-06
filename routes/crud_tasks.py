from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, update, delete
from sqlalchemy import select

from database.db_depends import get_db
from models.tasks import Task, Tag
# from models.tags import Tag
from schemas import CreateTask, TagCreate

router = APIRouter(prefix='/todo', tags=['task'])


#TODO: show tags
@router.get('/all_tasks')
async def get_all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


#TODO: tags
@router.post('/create_task', status_code=status.HTTP_201_CREATED)
async def create_task(db: Annotated[Session, Depends(get_db)],create_task: CreateTask):
    tags = create_task.tags
    existing_tags = db.query(Tag).filter(Tag.name.in_([tag.name for tag in tags])).all()

    existing_tag_names = [tag.name for tag in existing_tags]
    for tag in tags:
        if tag.name not in existing_tag_names:
            new_tag = Tag(name=tag.name)
            db.add(new_tag)
            db.commit()
            db.refresh(new_tag)

    new_task = Task(
        title=create_task.title,
        description=create_task.description,
        date_created=create_task.date_created,
        completed=create_task.completed
    )
    for tag in tags:
        tag_obj = db.query(Tag).filter(Tag.name == tag.name).first()
        if tag_obj:
            new_task.tags.append(tag_obj)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful',
        'task_id': new_task.id
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
