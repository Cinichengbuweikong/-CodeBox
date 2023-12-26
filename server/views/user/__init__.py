from fastapi import APIRouter

router = APIRouter(prefix="/user")

from . import index, projects, stars
