from fastapi import APIRouter


router = APIRouter(prefix="/stars")

from . import index
