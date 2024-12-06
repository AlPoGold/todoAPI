from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, update, delete
from sqlalchemy import select

from database.db_depends import get_db
from models.tasks import Task, Tag
from schemas import CreateTask

router = APIRouter(prefix='/todo', tags=['task'])


#TODO: show tags
@router.get('/all_tasks')
async def get_all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "date_created": task.date_created,
            "completed": task.completed,
            "tag": {
                "id": task.tag.id,
                "name": task.tag.name
            } if task.tag else None
        }
        for task in tasks
    ]

@router.get('/show_task')
async def get_task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no task'
        )
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "date_created": task.date_created,
        "completed": task.completed,
        "tag": {
            "id": task.tag.id,
            "name": task.tag.name
        } if task.tag else None
    }

@router.post('/create_task')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask):
    existing_tag = db.query(Tag).filter(Tag.name == create_task.tag.name).first()

    if not existing_tag:
        new_tag = Tag(name=create_task.tag.name)
        db.add(new_tag)
        db.flush()
        tag_id = new_tag.id
    else:
        tag_id = existing_tag.id
    new_task = Task(
        title=create_task.title,
        description=create_task.description,
        date_created=create_task.date_created,
        completed=create_task.completed,
        tag_id=tag_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful",
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "date_created": new_task.date_created,
        "completed": new_task.completed,
        "tag": {
            "id": tag_id,
            "name": create_task.tag.name
        }
    }

@router.put('/complete_task')
async def complete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
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
    if update_task.tag:
        existing_tag = db.scalar(select(Tag).where(Tag.name == update_task.tag.name))
        if not existing_tag:
            new_tag = Tag(name=update_task.tag.name)
            db.add(new_tag)
            db.flush()
            tag_id = new_tag.id
        else:
            tag_id = existing_tag.id
    else:
        tag_id = None

    db.execute(update(Task).where(Task.id == task_id).values(
        title=update_task.title,
        description=update_task.description,
        completed=update_task.completed,
        tag_id=tag_id
    ))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful'
    }


@router.delete('/delete_task')
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
        'transaction': 'Task is successful deleted'
    }
