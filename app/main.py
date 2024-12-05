from fastapi import FastAPI

from routes import tasks

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "My todo app"}

app.include_router(tasks.router)