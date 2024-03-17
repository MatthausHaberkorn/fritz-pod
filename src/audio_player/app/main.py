import contextlib
from fastapi import FastAPI

from .backend.settings import settings

from .backend.session import create_all_tables


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    if settings.debug:
        print(f"Loaded project with the following settings:\n{settings}")
    yield


app = FastAPI(lifespan=lifespan)
