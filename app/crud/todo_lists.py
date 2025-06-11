from app.schemas.todo_list import TodoListOut, list_serial
from app.models.todo_list import TodoList
from app.database.mongo import db
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError

async def get_todo_lists_service():
    todo_lists = await db.todo_lists.find().to_list(length=None)

    return list_serial(todo_lists)

async def create_todo_list_service(todo_list: TodoList):
    try:

        existing_list = await db.todo_lists.find_one({"title": todo_list.title})

        if existing_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A todo list with this title already exists."
            )

        result = await db.todo_lists.insert_one(todo_list.model_dump())

        return TodoListOut(id=str(result.inserted_id), **todo_list.model_dump())
    
    except HTTPException as e:
        raise e 

    # Handle specific database errors
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    # Handle other exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )