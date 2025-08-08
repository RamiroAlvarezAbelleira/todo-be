from pydantic import BaseModel, EmailStr

class User(BaseModel):
    uid: str
    username: str
    email: EmailStr
