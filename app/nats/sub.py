from app.nats import connect as c
import asyncio

from nats.aio.msg import Msg

shutdown_event = asyncio.Event()

async def users_sub():
    sub = await c.js.pull_subscribe("user.*", durable="users-service")
    while not shutdown_event.is_set():
        try:
            msgs = await sub.fetch(1, timeout=1)
            for msg in msgs:
                try:
                    data = msg.data.decode()
                    print(f"{msg.subject}: {data}")
                    await msg.ack()
                except Exception:
                    await msg.nak(delay=5)
        except TimeoutError:
            continue


async def items_sub():
    sub = await c.js.pull_subscribe("item.*", durable="items-service")
    while not shutdown_event.is_set():
        try:
            msgs = await sub.fetch(1, timeout=1)
            for msg in msgs:
                try:
                    data = msg.data.decode()
                    print(f"{msg.subject}: {data}")
                    await msg.ack()
                except Exception:
                    await msg.nak(delay=5)
        except TimeoutError:
            continue

