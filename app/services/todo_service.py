from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models.todo import Todo, TodoStatusEnum
from app.schemas.todo import TodoCreate, TodoUpdate
from datetime import datetime


def create_todo(db: Session, data: TodoCreate) -> Todo:
    todo = Todo(title=data.title, description=data.description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(db: Session, limit: int, offset: int, status: str = None,
              sort_by: str = "createdAt", order: str = "desc") -> (int, list[Todo]):
    query = db.query(Todo)
    if status:
        query = query.filter(Todo.status == status)

    total = query.count()

    order_func = desc if order == "desc" else asc
    # Handle camelCase to snake_case conversion for sorting
    sort_column = Todo.created_at if sort_by == "createdAt" else Todo.updated_at
    query = query.order_by(order_func(sort_column))

    todos = query.offset(offset).limit(limit).all()
    return total, todos


def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def update_todo(db: Session, todo_id: int, update_data: TodoUpdate):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return None
    
    # Extract values, handling potential Enum conversions
    update_dict = update_data.model_dump(exclude_unset=True)
    
    # Apply updates to model
    for key, value in update_dict.items():
        setattr(todo, key, value)
    
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return False
    db.delete(todo)
    db.commit()
    return True