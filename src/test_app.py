from contextlib import suppress

from fastapi import FastAPI

from .finelogging.exception import FineAsyncException, FineException
from .finelogging.logger import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

app = FastAPI()


@app.get("/")
async def read_root() -> dict:
    with suppress(FineException):
        raise FineException("Hello World")

    with suppress(FineAsyncException):
        raise FineAsyncException("Hello World")
    
    with suppress(FineAsyncException):
        await FineAsyncException.raise_exc("Hello World")
    return {"message": "Hello World"}
