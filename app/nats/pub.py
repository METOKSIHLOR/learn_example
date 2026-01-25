import json
from typing import Dict
from app.nats import connect as c

async def nats_publish(subject: str, data: dict) -> None:
    assert c.js is not None, "NATS is not initialized"

    await c.js.publish(
        subject,
        json.dumps(data).encode()
    )
    print(f"Published {subject} {data}")

