from typing import Optional
from pydantic import BaseModel, Field
from app.utils.py_object_id import PyObjectId

class Task(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    descriptionL: Optional[str] = None
    completed: bool = False
    todo_list_id: PyObjectId

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            PyObjectId: str
        }