from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_session, check_user_role
from app.api.schemas import UserCreateResponse, ItemSchema, ItemResponse
from app.db.models import Item
from app.db.repository import ItemRepository

router = APIRouter(prefix="/item", tags=["item"])

@router.get("/", response_model=List[ItemResponse])
async def get_items(session:AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    items = await repo.get_items()
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    item = await repo.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=ItemResponse, dependencies=[Depends(check_user_role)])
async def create_item(item: ItemSchema, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    item = await repo.create_item(item)
    await session.commit()
    return item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemSchema, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    item = await repo.update_item(item_id, item.model_dump(exclude_unset=True))
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.commit()
    return item

@router.delete("/{item_id}", dependencies=[Depends(check_user_role)])
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    await repo.delete_item(item_id)
    await session.commit()
    return {"success": True}


