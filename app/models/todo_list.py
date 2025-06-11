from typing import Optional
from pydantic import BaseModel, Field
from app.utils.py_object_id import PyObjectId

class TodoList(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str] = None

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            PyObjectId: str
        }