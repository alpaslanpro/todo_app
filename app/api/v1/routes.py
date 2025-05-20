from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.todo import TodoCreate, TodoListResponse, TodoResponse, TodoUpdate
from app.services import todo_service


router = APIRouter(tags=["Todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    created = todo_service.create_todo(db, todo)
    return created


@router.get("/todos", response_model=TodoListResponse)
def list_todos(
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0),
    status: str = Query(None),
    sortBy: str = Query("createdAt", regex="^(createdAt|updatedAt)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    total, todos = todo_service.get_todos(db, limit, offset, status, sortBy, order)
    if not todos:
        raise HTTPException(status_code=204, detail="No Content")
    return {"total": total, "limit": limit, "offset": offset, "data": todos}


@router.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_service.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, update_data: TodoUpdate, db: Session = Depends(get_db)):
    updated = todo_service.update_todo(db, todo_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated


@router.patch("/todos/{todo_id}", response_model=TodoResponse)
def patch_todo(todo_id: int, update_data: TodoUpdate, db: Session = Depends(get_db)):
    updated = todo_service.update_todo(db, todo_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    success = todo_service.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None