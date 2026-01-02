from fastapi import APIRouter

from .transcribe import transcribe

router_v1 = APIRouter(prefix="/v1")


router_v1.include_router(transcribe)
