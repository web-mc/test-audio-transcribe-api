from fastapi import FastAPI

from app.api import router_v1

app = FastAPI(
    title="AI Audio",
    version="0.1.0",
    root_path="/api",
    redoc_url=None,
)

app.include_router(router_v1)
