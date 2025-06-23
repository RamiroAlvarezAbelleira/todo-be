from fastapi import APIRouter
from app.models.task import Task
from app.crud.tasks import create_task_service, delete_task_service, toggle_complete_task_service, update_task_service, get_tasks_by_todo_list_id_service
from app.schemas.task import UpdateTask


router = APIRouter()

@router.post("/tasks")
async def create_task(task: Task):
    return await create_task_service(task)

@router.get("/tasks/{todo_list_id}")
async def get_tasks_by_todo_list_id(todo_list_id: str):
    return await get_tasks_by_todo_list_id_service(todo_list_id)

@router.put("/tasks/{task_id}")
async def update_task(task_id: str, task_data: UpdateTask):
    return await update_task_service(task_id, task_data)

@router.put("/tasks/toggle_complete/{task_id}")
async def toggle_complete_task(task_id: str):
    return await toggle_complete_task_service(task_id)

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    return await delete_task_service(task_id)