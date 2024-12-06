from fastapi import FastAPI

from routes import crud_tasks, filter_tasks

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "My todo app"}

app.include_router(crud_tasks.router)
app.include_router(filter_tasks.router)