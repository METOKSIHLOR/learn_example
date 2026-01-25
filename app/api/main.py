from fastapi import FastAPI

from app.api.routers.users import router as user_router
from app.api.routers.items import router as item_router
from app.db.session import close_db, connect_db
from app.nats.connect import create_nats, close_nats
from app.nats.sub import users_sub, items_sub


async def lifespan(app: FastAPI):
    await connect_db()
    await create_nats()
    await users_sub()
    await items_sub()
    yield
    await close_db()
    await close_nats()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(item_router)

