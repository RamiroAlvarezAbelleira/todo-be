from fastapi import FastAPI
from app.database.mongo import client

app = FastAPI()

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