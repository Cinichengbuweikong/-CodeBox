from fastapi import APIRouter


router = APIRouter(prefix="/code")

from . import index, _cid
