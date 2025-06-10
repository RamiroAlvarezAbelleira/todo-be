from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from app.utils.py_object_id import PyObjectId

class TodoList(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }