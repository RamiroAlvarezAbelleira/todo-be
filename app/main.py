from fastapi import FastAPI
from app.database.mongo import client
from app.routers import todo_lists, tasks, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Orígenes permitidos
origins = [
    "http://localhost:3000",  # Next.js
    "http://127.0.0.1:3000",  # Por si usás esta dirección también
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # Permite esos orígenes
    allow_credentials=True,
    allow_methods=["*"],                # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],                # Permite todos los headers
)

\
app.include_router(todo_lists.router, prefix="/api", tags=["Todo Lists"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])
app.include_router(users.router, prefix="/api", tags=["Users"] )

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/ping-mongo")
async def ping_mongo():
    try:
        await client.admin.command("ping")
        return {"message": "MongoDB is reachable"}
    except Exception as e:
        return {"error": str(e)}