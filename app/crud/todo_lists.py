from app.models.todo_list import TodoList
from app.schemas.todo_list import TodoListCreate, TodoListOut
from app.database.mongo import db

async def create_todo_list_service(todo_list: TodoListCreate):
    new_todo_list = TodoList(**todo_list.model_dump())
    result = await db.todo_lists.insert_one(new_todo_list.model_dump(by_alias=True))

    return TodoListOut(id=str(result.inserted_id), **new_todo_list.model_dump(by_alias=True))