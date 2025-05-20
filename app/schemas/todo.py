from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class TodoStatus(str, Enum):
    new = "new"
    in_progress = "in-progress"
    completed = "completed"


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TodoStatus]


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TodoStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TodoListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: list[TodoResponse]
