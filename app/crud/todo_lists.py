from app.models.todo_list import TodoList
from app.schemas.todo_list import TodoListCreate, TodoListOut
from app.database.mongo import db
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError

async def create_todo_list_service(todo_list: TodoListCreate):
    try:

        existing_list = await db.todo_lists.find_one({"title": todo_list.title})

        if existing_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A todo list with this title already exists."
            )
        
        new_todo_list = TodoList(**todo_list.model_dump())

        result = await db.todo_lists.insert_one(new_todo_list.model_dump(by_alias=True))

        return TodoListOut(id=str(result.inserted_id), **new_todo_list.model_dump(by_alias=True))
    
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