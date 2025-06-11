from typing import Optional
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    todo_list_id: str