from typing import Optional
from pydantic import BaseModel, Field

class TodoListOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None

class TodoListUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None

def individual_serial(todo_list) -> dict:
    return {
        "id": str(todo_list["_id"]),
        "title": todo_list["title"],
        "description": todo_list.get("description")
    }

def list_serial(todo_lists) -> list:
    return [individual_serial(todo_list) for todo_list in todo_lists]