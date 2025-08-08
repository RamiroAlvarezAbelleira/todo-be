from fastapi import APIRouter
from app.models.user import User
from app.crud.users import create_user_service


router = APIRouter()

@router.post("/users")
async def create_user(user: User):
    return await create_user_service(user)