from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models.todo import Todo, TodoStatusEnum
from app.schemas.todo import TodoCreate


def create_todo(db: Session, data: TodoCreate) -> Todo:
    todo = Todo(title=data.title, description=data.description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(db: Session, limit: int, offset: int, status: str = None,
              sort_by: str = "created_at", order: str = "desc") -> (int, list[Todo]):
    query = db.query(Todo)
    if status:
        query = query.filter(Todo.status == status)

    total = query.count()

    order_func = desc if order == "desc" else asc
    if sort_by == "createdAt":
        query = query.order_by(order_func(Todo.created_at))
    elif sort_by == "updatedAt":
        query = query.order_by(order_func(Todo.updated_at))

    todos = query.offset(offset).limit(limit).all()
    return total, todos
