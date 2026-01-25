from nats.aio.client import Client as NATS
from nats.js import JetStreamContext

nc: NATS | None = None
js: JetStreamContext | None = None

async def create_nats():
    global nc, js
    nc = NATS()

    await nc.connect("nats://localhost:4222")

    js = nc.jetstream()

async def close_nats():
    if nc:
        await nc.drain()