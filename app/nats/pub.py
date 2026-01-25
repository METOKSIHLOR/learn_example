import json
from typing import Dict
from app.nats.connect import js

async def publish(subject: str, data: Dict) -> None:
    assert js is not None, "NATS is not initialized"

    await js.publish(
        subject,
        json.dumps(data).encode()
    )

    print(f"Published {subject} {data}")

