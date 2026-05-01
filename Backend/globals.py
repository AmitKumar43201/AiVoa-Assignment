from fastapi import WebSocket

client: WebSocket | None = None
db_pool = None

async def emit(event: str, data: dict):
    if client is None:
        print(f"No client connected, dropping event: {event}")
        return
    await client.send_json({"event": event, "data": data})