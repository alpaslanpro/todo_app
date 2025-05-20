from fastapi import APIRouter, Depends, HTTPException, status, Query, Response, Request
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.todo import TodoCreate, TodoListResponse, TodoResponse, TodoUpdate
from app.services import todo_service
from typing import Optional


router = APIRouter(tags=["Todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, response: Response, request: Request, db: Session = Depends(get_db)):
    created = todo_service.create_todo(db, todo)
    # Set Location header as per specification
    response.headers["Location"] = f"{request.url.path}/{created.id}"
    return created


@router.get("/todos", response_model=Optional[TodoListResponse])
def list_todos(
    response: Response,
    limit: int = Query(20, ge=1, description="Maximum number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    status_filter: Optional[str] = Query(
        None, 
        alias="status",
        description="Filter todos by status (new, in-progress, completed)"
    ),
    sortBy: str = Query(
        "createdAt", 
        regex="^(createdAt|updatedAt)$",
        description="Field to sort by"
    ),
    order: str = Query(
        "desc", 
        regex="^(asc|desc)$",
        description="Sort order (ascending or descending)"
    ),
    db: Session = Depends(get_db)
):
    total, todos = todo_service.get_todos(db, limit, offset, status_filter, sortBy, order)
    
    if not todos:
        response.status_code = status.HTTP_204_NO_CONTENT
        return None
        
    return {"total": total, "limit": limit, "offset": offset, "data": todos}


@router.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_service.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )
    return todo


@router.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, update_data: TodoUpdate, db: Session = Depends(get_db)):
    updated = todo_service.update_todo(db, todo_id, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )
    return updated


@router.patch("/todos/{todo_id}", response_model=TodoResponse)
def patch_todo(todo_id: int, update_data: TodoUpdate, db: Session = Depends(get_db)):
    if not update_data.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
        
    updated = todo_service.update_todo(db, todo_id, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )
    return updated


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    success = todo_service.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )
    return None


# Additional status transition endpoints
@router.post("/todos/{todo_id}/complete", response_model=TodoResponse)
def complete_todo(todo_id: int, db: Session = Depends(get_db)):
    from app.models.todo import TodoStatusEnum
    
    todo = todo_service.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )
    
    # Use the update_status function
    updated_todo = todo_service.update_status(db, todo_id, TodoStatusEnum.completed)
    return updated_todo


@router.post("/todos/{todo_id}/in-progress", response_model=TodoResponse)
def mark_in_progress(todo_id: int, db: Session = Depends(get_db)):
    from app.models.todo import TodoStatusEnum
    
    todo = todo_service.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
        )
    
    # Use the update_status function
    updated_todo = todo_service.update_status(db, todo_id, TodoStatusEnum.in_progress)
    return updated_todo