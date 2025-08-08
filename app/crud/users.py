from app.models.user import User
from app.database.mongo import db
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError
from app.schemas.user import UserOut

async def create_user_service(user: User):
    try:
        existing_user = await db.users.find_one(
            {"$or": [{"uid": user.uid}, {"email": user.email}]}
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or UID already exists"
            )

        result = await db.users.insert_one(user.model_dump())

        return UserOut(id=str(result.inserted_id), **user.model_dump())
    
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