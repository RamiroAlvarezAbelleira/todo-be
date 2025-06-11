from fastapi import APIRouter
from app.models.task import Task
from app.crud.tasks import create_task_service, delete_task_service

router = APIRouter()

@router.post("/tasks")
async def create_task(task: Task):
    return await create_task_service(task)

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    return await delete_task_service(task_id)