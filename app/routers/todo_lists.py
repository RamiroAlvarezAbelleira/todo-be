from fastapi import APIRouter
from app.models.todo_list import TodoList
from app.crud.todo_lists import create_todo_list_service, get_todo_lists_service

router = APIRouter()

@router.get("/todo_lists")
async def get_todo_lists():
    return await get_todo_lists_service()

@router.post("/todo-lists")
async def create_todo_list(todo_list: TodoList):
    return await create_todo_list_service(todo_list)