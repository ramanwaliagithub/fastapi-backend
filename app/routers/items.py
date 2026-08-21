from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


@router.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@router.get("")
async def list_items(skip: int = 0, limit: int = 10, search: str | None = None):
    return {"skip": skip, "limit": limit, "search": search}


@router.post("")
async def create_item(item: Item):
    return item
