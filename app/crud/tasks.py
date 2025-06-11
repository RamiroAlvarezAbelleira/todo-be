from app.models.task import Task
from app.database.mongo import db
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError
from bson import ObjectId
from app.schemas.task import TaskOut

async def create_task_service(task: Task):
    try:
        if not ObjectId.is_valid(task.todo_list_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid todo list ID format."
            )
        
        todo_list = await db.todo_lists.find_one({"_id": ObjectId(task.todo_list_id)})

        if not todo_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo list not found."
            )
        

        result = await db.tasks.insert_one(task.model_dump())

        return TaskOut(id=str(result.inserted_id), **task.model_dump())
    
    except Exception as e:
        raise e
    
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )