from fastapi import FastAPI

from .config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/")
async def root():
    return {"message": "TaskFlow API is running"}
