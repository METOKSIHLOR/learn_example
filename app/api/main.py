from fastapi import FastAPI

from app.api.routers.users import router as user_router
from app.api.routers.items import router as item_router
from app.db.session import close_db, connect_db
from app.nats.connect import close_nats, init_nats_system
from app.nats.sub import shutdown_event


async def lifespan(app: FastAPI):
    await connect_db()
    await init_nats_system()

    yield

    await close_db()

    shutdown_event.set()
    await close_nats()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(item_router)

