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
    
async def delete_task_service(task_id: str):
    try:
        if not ObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID format."
            )
        
        result = await db.tasks.delete_one({"_id": ObjectId(task_id)})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found."
            )
        
        return {"detail": "Task deleted successfully."}
    
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
    
async def toggle_complete_task_service(task_id: str):
    try:
        if not ObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID format."
            )
        
        task = await db.tasks.find_one({"_id": ObjectId(task_id)})

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found."
            )
        
        new_completed_status = not task.get("completed", False)

        result = await db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"completed": new_completed_status}}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found."
            )
        
        updated_task = await db.tasks.find_one({"_id": ObjectId(task_id)})

        return TaskOut(id=str(updated_task["_id"]), **updated_task)
    
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