from typing import Optional
from pydantic import BaseModel

class TodoListCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoListOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None