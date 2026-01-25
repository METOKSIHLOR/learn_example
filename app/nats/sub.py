from app.nats.connect import js
import asyncio

from nats.aio.msg import Msg


async def users_sub():
    async def users_handler(msg: Msg) -> None:
        try:
            sub = msg.subject
            data = msg.data.decode()
            print(f"{sub}: {data}")
            await msg.ack()
        except Exception:
            await msg.nak(delay=5)

    await js.subscribe("user.*", cb=users_handler, durable="user-service")

async def items_sub():
    async def items_handler(msg: Msg) -> None:
        try:
            sub = msg.subject
            data = msg.data.decode()
            print(f"{sub}: {data}")
            await msg.ack()
        except Exception:
            await msg.nak(delay=5)

    await js.subscribe("item.*", cb=items_handler, durable="items-service")


