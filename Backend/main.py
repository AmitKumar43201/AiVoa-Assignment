from fastapi import FastAPI,WebSocket, WebSocketDisconnect
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
import globals as g
from app.db.connection import connect_db, close_db
from app.controlers.agent_controlers import agent_routes
from app.controlers.db_controlers import db_roots

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    g.client = ws  # update globals.py client, not main.py's
    await ws.accept()
    print("Client connected")

    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        g.client = None
        print("Client disconnected")
app.include_router(agent_routes)
app.include_router(db_roots)
   
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    