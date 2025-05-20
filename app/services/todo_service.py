from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models.todo import Todo, TodoStatusEnum
from app.schemas.todo import TodoCreate, TodoUpdate
from datetime import datetime
from typing import Optional, Tuple, List


def create_todo(db: Session, data: TodoCreate) -> Todo:
    """
    Create a new todo item in the database
    
    Args:
        db: Database session
        data: Todo creation data
        
    Returns:
        Created todo object
    """
    todo = Todo(
        title=data.title, 
        description=data.description,
        status=TodoStatusEnum.new  # Explicitly set default status
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(
    db: Session, 
    limit: int, 
    offset: int, 
    status: Optional[str] = None,
    sort_by: str = "createdAt", 
    order: str = "desc"
) -> Tuple[int, List[Todo]]:
    """
    Get todos with filtering, sorting and pagination
    
    Args:
        db: Database session
        limit: Maximum number of items to return
        offset: Number of items to skip
        status: Filter by status (optional)
        sort_by: Field to sort by (createdAt or updatedAt)
        order: Sort order (asc or desc)
        
    Returns:
        Tuple of (total count, list of todos)
    """
    query = db.query(Todo)
    
    # Apply status filter if provided
    if status:
        query = query.filter(Todo.status == status)

    # Get total count before pagination
    total = query.count()

    # Apply sorting
    order_func = desc if order == "desc" else asc
    # Handle camelCase to snake_case conversion for sorting
    sort_column = Todo.created_at if sort_by == "createdAt" else Todo.updated_at
    query = query.order_by(order_func(sort_column))

    # Apply pagination
    todos = query.offset(offset).limit(limit).all()
    return total, todos


def get_todo(db: Session, todo_id: int) -> Optional[Todo]:
    """
    Get a todo by ID
    
    Args:
        db: Database session
        todo_id: Todo ID
        
    Returns:
        Todo object or None if not found
    """
    return db.query(Todo).filter(Todo.id == todo_id).first()


def update_todo(db: Session, todo_id: int, update_data: TodoUpdate) -> Optional[Todo]:
    """
    Update a todo
    
    Args:
        db: Database session
        todo_id: Todo ID
        update_data: Data to update
        
    Returns:
        Updated todo or None if not found
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return None
    
    # Extract values, handling potential Enum conversions
    update_dict = update_data.model_dump(exclude_unset=True)
    
    # Apply updates to model
    for key, value in update_dict.items():
        setattr(todo, key, value)
    
    # Update the updated_at timestamp
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo


def update_status(db: Session, todo_id: int, status: TodoStatusEnum) -> Optional[Todo]:
    """
    Update todo status
    
    Args:
        db: Database session
        todo_id: Todo ID
        status: New status
        
    Returns:
        Updated todo or None if not found
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return None
    
    todo.status = status
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int) -> bool:
    """
    Delete a todo
    
    Args:
        db: Database session
        todo_id: Todo ID
        
    Returns:
        True if deleted, False if not found
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return False
    db.delete(todo)
    db.commit()
    return True