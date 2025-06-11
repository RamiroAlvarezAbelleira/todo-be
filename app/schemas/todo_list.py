from typing import Optional, Annotated
from pydantic import BaseModel, StringConstraints

class TodoListCreate(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    description: Optional[str] = None

class TodoListOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None