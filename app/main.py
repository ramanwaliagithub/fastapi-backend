from fastapi import FastAPI

from .routers import items

app = FastAPI()

app.include_router(items.router)


@app.get("/")
async def root():
    return {"message": "TaskFlow API is running"}
