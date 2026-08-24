"""
Frozen snapshot of the "items" demo router built across Days 2-5 while learning path/query
params, request bodies, response models, status codes, and HTTPException. Retired from the
running app on Day 6 once those concepts were understood — kept here for reference only.
Not imported by app/main.py; not maintained going forward.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/items", tags=["items"])


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemOut(ItemCreate):
    id: int

_items: dict[int, ItemOut] = {}
_next_id = 1


@router.get("/{item_id}", response_model=ItemOut)
async def read_item(item_id: int):
    item = _items.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {item_id} not found"
        )
    return item


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
