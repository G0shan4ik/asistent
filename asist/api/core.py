from contextlib import asynccontextmanager
from fastapi import FastAPI
from uvicorn import Config, Server

from asist.database.core import init_database

from os import getenv
from dotenv import load_dotenv


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield


app = FastAPI(
    debug=bool(getenv("DEBUG", True)),
    lifespan=lifespan
)

async def run_api():
    config = Config(
        app=app,
        host="127.0.0.1",
        port=8000,
        reload=bool(getenv("DEBUG", False)),
        log_level="info" if getenv("DEBUG") else "warning"
    )
    server = Server(config)
    await server.serve()

__all__ = [
    "app", "run_api"
]