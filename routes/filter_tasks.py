from fastapi import APIRouter, Depends, status, HTTPException, Query

from sqlalchemy.orm import Session
from typing import Annotated, Optional
from sqlalchemy import insert, update, delete, asc, desc
from sqlalchemy import select
from slugify import slugify

from database.db_depends import get_db
from models.tasks import Task, Tag
from schemas import CreateTask, PaginatedResponse

router = APIRouter(prefix='/todo', tags=['filter'])

#TODO: add filtration by tags
@router.get("/tasks/filter", response_model=PaginatedResponse)
def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter settings"),
    tag_name: Optional[str] = Query(None, description="Filter by tag"),
    sort_by: Optional[str] = Query("date_created", regex="^(title|date_created)$", description="Sorting"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$", description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=10, description="Size page"),
    db: Session = Depends(get_db),
):
    query = db.query(Task)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if tag_name:
        query = query.join(Tag).filter(Tag.name.ilike(f"%{tag_name}%"))

    order_func = asc if order == "asc" else desc
    if sort_by == "title":
        query = query.order_by(order_func(Task.title))
    elif sort_by == "date_created":
        query = query.order_by(order_func(Task.date_created))

    total = query.count()
    tasks = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        page=page,
        page_size=page_size,
        total=total,
        tasks=tasks
    )

