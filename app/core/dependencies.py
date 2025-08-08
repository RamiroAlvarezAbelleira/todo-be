from fastapi import Header
from app.core.firebase import verify_firebase_token
from fastapi import HTTPException, status

async def get_current_user_uid(authorization: str = Header(...)):
    """
    Extrae el token del header Authorization (Bearer token),
    valida y devuelve el uid del usuario.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    token = authorization.split(" ")[1]
    uid = verify_firebase_token(token)
    return uid
