from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user_uid
from app.models.task import Task
from app.crud.tasks import create_task_service, delete_task_service, toggle_complete_task_service, update_task_service, get_tasks_by_todo_list_id_service
from app.schemas.task import UpdateTask, CreateTask


router = APIRouter()

@router.post("/tasks")
async def create_task(task: CreateTask, user_uid: str = Depends(get_current_user_uid)):
    return await create_task_service(task, user_uid)

@router.get("/tasks/{todo_list_id}")
async def get_tasks_by_todo_list_id(todo_list_id: str, user_uid: str = Depends(get_current_user_uid)):
    return await get_tasks_by_todo_list_id_service(todo_list_id, user_uid)

@router.put("/tasks/{task_id}")
async def update_task(task_id: str, task_data: UpdateTask, user_uid: str = Depends(get_current_user_uid)):
    return await update_task_service(task_id, task_data, user_uid)

@router.put("/tasks/toggle_complete/{task_id}")
async def toggle_complete_task(task_id: str, user_uid: str = Depends(get_current_user_uid)):
    return await toggle_complete_task_service(task_id, user_uid)

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, user_uid: str = Depends(get_current_user_uid)):
    return await delete_task_service(task_id, user_uid)