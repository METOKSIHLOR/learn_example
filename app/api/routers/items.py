from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks

from app.api.dependencies import get_session, check_user_role
from app.api.schemas import ItemSchema, ItemResponse
from app.db.repository import ItemRepository
from app.nats.pub import nats_publish

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
async def create_item(background_tasks: BackgroundTasks, item: ItemSchema, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    item = await repo.create_item(item)
    await session.commit()

    data = {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "in_stock": item.in_stock,
    }

    background_tasks.add_task(nats_publish, "item.create", data)
    return item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(background_tasks: BackgroundTasks, item_id: int, item: ItemSchema, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    old_item = await repo.get_item(item_id)
    if old_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = await repo.update_item(item_id, item.model_dump(exclude_unset=True))
    await session.commit()

    data = {"old_item": ItemResponse.from_orm(old_item).model_dump(),
        "new_item": ItemResponse.from_orm(updated_item).model_dump()
}

    background_tasks.add_task(nats_publish, "item.update", data)
    return updated_item

@router.delete("/{item_id}", dependencies=[Depends(check_user_role)])
async def delete_item(background_tasks: BackgroundTasks, item_id: int, session: AsyncSession = Depends(get_session)):
    repo = ItemRepository(session)
    await repo.delete_item(item_id)
    await session.commit()

    background_tasks.add_task(nats_publish, "item.delete", {"deleted_item": item_id})
    return {"success": True}


