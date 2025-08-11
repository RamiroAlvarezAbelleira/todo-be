from app.schemas.todo_list import TodoListOut, TodoListUpdate, list_serial, individual_serial
from app.database.mongo import db
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError
from bson import ObjectId

async def get_todo_lists_service(user_uid: str):
    todo_lists = await db.todo_lists.find(
        {"user_uid": user_uid}
    ).to_list(length=None)

    return list_serial(todo_lists)

async def get_todo_list_by_id_service(todo_list_id: str, user_uid: str):
    try:
        # Validate the ObjectId format
        if not ObjectId.is_valid(todo_list_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid todo list ID format."
            )
        
        todo_list = await db.todo_lists.find_one({"_id": ObjectId(todo_list_id)})

        # If the todo list is not found, raise a 404 error
        if not todo_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo list not found."
            )
        
        serialized_todo_list = individual_serial(todo_list)
        
        return serialized_todo_list

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

async def create_todo_list_service(todo_list: TodoListUpdate, user_uid: str):
    try:
        # Convertir a dict para poder modificarlo
        todo_list_data = todo_list.model_dump()
        
        # Sobrescribimos/aseguramos el user_uid
        todo_list_data["user_uid"] = user_uid

        existing_list = await db.todo_lists.find_one({"title": todo_list.title})

        if existing_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A todo list with this title already exists."
            )

        result = await db.todo_lists.insert_one(todo_list_data)

        return TodoListOut(id=str(result.inserted_id), **todo_list_data)
    
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


async def update_todo_list_service(todo_list_id: str, update_data: TodoListUpdate, user_uid: str):
    try:
        if not ObjectId.is_valid(todo_list_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid todo list ID format."
            )

        update_data_dict = update_data.model_dump(exclude_unset=True)

        if not update_data_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid data provided for update."
            )

        result = await db.todo_lists.update_one(
            {"_id": ObjectId(todo_list_id), "user_uid": user_uid},
            {"$set": update_data_dict}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo list not found."
            )

        updated_todo_list = await db.todo_lists.find_one({"_id": ObjectId(todo_list_id)})

        return individual_serial(updated_todo_list)

    except HTTPException as e:
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


async def delete_todo_list_service(todo_list_id: str, user_uid: str):
    try:
        if not ObjectId.is_valid(todo_list_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid todo list ID format."
            )
        todo_list = await db.todo_lists.find_one({
            "_id": ObjectId(todo_list_id),
            "user_uid": user_uid
        })

        if not todo_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo list not found or you don't have permission to delete it."
            )
        # First, delete all tasks associated with the todo list
        
        await db.tasks.delete_many({"todo_list_id": todo_list_id})

        # Then delete the todo list

        result = await db.todo_lists.delete_one({"_id": ObjectId(todo_list_id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo list not found."
            )
        return {"message": "Todo list deleted successfully."}
    except HTTPException as e:
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