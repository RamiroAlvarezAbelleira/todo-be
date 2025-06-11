from pydantic import BaseModel
from typing import Optional

class TaskOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    todo_list_id: str

def individual_task_serial(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task.get("description", ""),
        "completed": task.get("completed", False),
        "todo_list_id": str(task["todo_list_id"])
    }

def list_task_serial(tasks) -> list:
    return [individual_task_serial(task) for task in tasks]