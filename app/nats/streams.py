from nats.js.api import StreamConfig
from app.nats.connect import js

async def users_stream():
    await js.add_stream(
        StreamConfig(
            name="USERS",
            subjects=["user.*"],
            max_age=7 * 24 * 3600,
        )
    )
    print("Users stream created")

async def items_stream():
    await js.add_stream(
        StreamConfig(
            name="ITEMS",
            subjects=["item.*"],
            max_age=7 * 24 * 3600,
        )
    )
    print("Items stream created")

