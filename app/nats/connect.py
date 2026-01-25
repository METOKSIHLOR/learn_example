from nats.aio.client import Client as NATS
from nats.js import JetStreamContext

from app.nats.streams import users_stream, items_stream
from app.nats.sub import users_sub, items_sub
import asyncio

nc: NATS | None = None
js: JetStreamContext | None = None

async def create_nats():
    global nc, js
    nc = NATS()

    await nc.connect("nats://localhost:4222")

    js = nc.jetstream()

async def close_nats():
    if nc:
        await nc.close()

async def init_nats_system():
    await create_nats()
    await users_stream()
    await items_stream()

    #pull consumers в фоне
    asyncio.create_task(users_sub())
    asyncio.create_task(items_sub())