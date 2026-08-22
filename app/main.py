from fastapi import FastAPI
from .config import settings

from .routers import items

# app = FastAPI()
app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(items.router)


@app.get("/")
async def root():
    return {"message": "TaskFlow API is running"}
