import os

from fastapi import Depends, FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_current_user
from .routes import entity, entity_type

ENVIRONMENT = os.environ.get("ENVIRONMENT", "")

root_prefix = f""

PROTECTED = [Depends(get_current_user)]

app = FastAPI(
    title="Registry Service",
    description="registry description",
    version="0.0.1",
    root_path=root_prefix,
)
app.include_router(entity_type.router, dependencies=PROTECTED)
app.include_router(entity.router, dependencies=PROTECTED)

add_pagination(app)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def version():
    return {"message": "registry service"}
