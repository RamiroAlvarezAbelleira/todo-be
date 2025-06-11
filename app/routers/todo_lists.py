from fastapi import APIRouter
from app.schemas.todo_list import TodoListCreate
from app.crud.todo_lists import create_todo_list_service

router = APIRouter()

@router.post("/todo-lists")
async def create_todo_list(todo_list: TodoListCreate):
    return await create_todo_list_service(todo_list)