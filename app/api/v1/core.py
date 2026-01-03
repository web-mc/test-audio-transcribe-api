from fastapi import APIRouter

from .transcriptions import transcriptions

router_v1 = APIRouter(prefix="/v1")


router_v1.include_router(transcriptions)
