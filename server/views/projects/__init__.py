from fastapi import APIRouter


router = APIRouter(prefix="/projects")

from . import index, temporaryproject
from ._pid import router as _pidRouter


router.include_router(_pidRouter)
