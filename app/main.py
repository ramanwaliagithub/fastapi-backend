from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "TaskFlow API is running"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10, search: str | None = None):
    return {"skip": skip, "limit": limit, "search": search}