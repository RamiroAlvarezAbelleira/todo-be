from app.models.task import Task
from app.database.mongo import db
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError
from bson import ObjectId
from app.schemas.task import TaskOut, individual_task_serial, list_task_serial, UpdateTask, CreateTask

async def create_task_service(task: CreateTask, user_uid: str):
    try:
        if not ObjectId.is_valid(task.todo_list_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid todo list ID format."
            )
        
        task_data = task.model_dump()
        task_data["user_uid"] = user_uid
        
        todo_list = await db.todo_lists.find_one({"_id": ObjectId(task.todo_list_id), "user_uid": user_uid})

        if not todo_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo list not found."
            )
        

        result = await db.tasks.insert_one(task_data)

        return TaskOut(id=str(result.inserted_id), **task_data)
    
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

async def get_tasks_by_todo_list_id_service(todo_list_id: str, user_uid: str):
    try:
        if not ObjectId.is_valid(todo_list_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid todo list ID format."
            )
        
        tasks = await db.tasks.find({"todo_list_id": todo_list_id, "user_uid": user_uid}).to_list(length=None)
        serialized_tasks = list_task_serial(tasks)

        return serialized_tasks
    
    except Exception as e:
        raise e
    
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
async def update_task_service(task_id: str, task_data: UpdateTask, user_uid: str):
    try:
        if not ObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID format."
            )

        update_fields = {}

        if task_data.title and task_data.description:
            update_fields = {
                "title": task_data.title,
                "description": task_data.description,
            }
        elif task_data.title:
            update_fields = {"title": task_data.title}
        elif task_data.description:
            update_fields = {"description": task_data.description}


        await db.tasks.update_one(
            {"_id": ObjectId(task_id), "user_uid": user_uid},
            {"$set": update_fields}
            )
        updated_task = await db.tasks.find_one({"_id": ObjectId(task_id)})

        return individual_task_serial(updated_task)
    
    except Exception as e:
        raise e
    
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
async def delete_task_service(task_id: str, user_uid: str):
    try:
        if not ObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID format."
            )
        
        result = await db.tasks.delete_one({"_id": ObjectId(task_id), "user_uid": user_uid})

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
    
async def toggle_complete_task_service(task_id: str, user_uid: str):
    try:
        if not ObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task ID format."
            )
        
        task = await db.tasks.find_one({"_id": ObjectId(task_id), "user_uid": user_uid})

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