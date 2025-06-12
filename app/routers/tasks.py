from fastapi import APIRouter
from app.models.task import Task
from app.crud.tasks import create_task_service, delete_task_service, toggle_complete_task_service, update_task_service

router = APIRouter()

@router.post("/tasks")
async def create_task(task: Task):
    return await create_task_service(task)

@router.put("/tasks/{task_id}")
async def update_task(task_id: str, task_data: Task):
    return await update_task_service(task_id, task_data)

@router.put("/tasks/toggle_complete/{task_id}")
async def toggle_complete_task(task_id: str):
    return await toggle_complete_task_service(task_id)

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    return await delete_task_service(task_id)