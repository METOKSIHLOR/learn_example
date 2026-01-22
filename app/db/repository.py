from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.autorization.hash import hash_password
from app.api.schemas import UserCreate, ItemSchema
from app.db.models import User, Item


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, schema: UserCreate):
        hashed_password = hash_password(schema.password)
        user = User(
            username=schema.username,
            password_hash=hashed_password,
            role=schema.role
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_user_by_id(self,  user_id: int):
        stmt = select(User).where(User.id == int(user_id))
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_item(self, schema: ItemSchema):
        item = Item(name=schema.name, price=schema.price, in_stock=schema.in_stock)
        self.session.add(item)
        await self.session.flush()
        return item

    async def get_items(self):
        stmt = select(Item).order_by(Item.id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_item(self, item_id: int):
        stmt = select(Item).where(Item.id == item_id)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def update_item(self, item_id: int, data: dict):
        item = await self.get_item(item_id)

        if item is None:
            return None

        for key, value in data.items():
            if value is not None:
                setattr(item, key, value)

        await self.session.flush()
        return item

    async def delete_item(self, item_id: int):
        stmt = delete(Item).where(Item.id == item_id)
        await self.session.execute(stmt)
        await self.session.flush()
        return
