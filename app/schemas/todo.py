from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List


class TodoStatus(str, Enum):
    new = "new"
    in_progress = "in-progress"
    completed = "completed"
    

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TodoStatus] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    createdAt: datetime = Field(alias="created_at")
    updatedAt: datetime = Field(alias="updated_at")

    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Get milk and bread",
                "status": "new",
                "createdAt": "2023-05-20T12:00:00",
                "updatedAt": "2023-05-20T12:00:00"
            }
        }


class TodoListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[TodoResponse]