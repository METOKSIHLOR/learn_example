from nats.js.api import StreamConfig
from app.nats import connect as c
from nats.js.errors import ObjectAlreadyExists

async def users_stream():
    try:
        await c.js.add_stream(
            StreamConfig(
                name="USERS",
                subjects=["user.*"],
                max_age=7 * 24 * 3600,
            )
        )
    except ObjectAlreadyExists:
        print("Users stream already exists, skipping")
    else:
        print("Users stream created")

async def items_stream():
    try:
        await c.js.add_stream(
            StreamConfig(
                name="ITEMS",
                subjects=["item.*"],
                max_age=7 * 24 * 3600,
            )
        )
    except ObjectAlreadyExists:
        print("Users stream already exists, skipping")
    else:
        print("Items stream created")

