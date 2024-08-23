from fastapi import FastAPI
from .routes.routes import websocket_endpoint

app = FastAPI()

app.include_router(websocket_endpoint, prefix="/ws")
