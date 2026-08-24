from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, status

router = APIRouter(prefix="/items", tags=["items"])


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemOut(ItemCreate):
    id: int

_items: dict[int, ItemOut] = {}
_next_id = 1

    
@router.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@router.get("")
async def list_items(skip: int = 0, limit: int = 10, search: str | None = None):
    return {"skip": skip, "limit": limit, "search": search}


@router.post("", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    global _next_id
    new_item = ItemOut(id=_next_id, **item.model_dump())
    _items[_next_id] = new_item
    _next_id += 1
    return new_item
