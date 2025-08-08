import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, status
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SERVICE_ACCOUNT_PATH = BASE_DIR / "firebase-service-account-todo-app.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))
    firebase_admin.initialize_app(cred)

def verify_firebase_token(token: str) -> str:
    """
    Verifica el token de Firebase y devuelve el uid del usuario.
    """
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token.get("uid")
        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: UID not found",
            )
        return uid
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation error: {str(e)}"
        )

