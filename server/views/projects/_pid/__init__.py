from fastapi import APIRouter


router = APIRouter(prefix="/{pid:int}")

from . import index, comments
from .code import router as codeRouter


router.include_router(codeRouter)
