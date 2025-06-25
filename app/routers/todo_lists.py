from fastapi import APIRouter
from app.models.todo_list import TodoList
from app.schemas.todo_list import TodoListUpdate
from app.crud.todo_lists import create_todo_list_service, get_todo_lists_service, get_todo_list_by_id_service, delete_todo_list_service, update_todo_list_service

router = APIRouter()

@router.get("/todo-lists")
async def get_todo_lists():
    return await get_todo_lists_service()

@router.post("/todo-lists")
async def create_todo_list(todo_list: TodoList):
    return await create_todo_list_service(todo_list)

@router.put("/todo-lists/{todo_list_id}")
async def update_todo_list(todo_list_id: str, update_data: TodoListUpdate):
    return await update_todo_list_service(todo_list_id, update_data)

@router.get("/todo-lists/{todo_list_id}")
async def get_todo_list(todo_list_id: str):
    return await get_todo_list_by_id_service(todo_list_id)

# Recordar que cuando agregue los tasks tambien tengo que borrarlos antes de borrar la lista
@router.delete("/todo-lists/{todo_list_id}")
async def delete_todo_list(todo_list_id: str):
    return await delete_todo_list_service(todo_list_id)