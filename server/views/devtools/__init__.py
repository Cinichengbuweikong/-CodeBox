from views import server
from fastapi import APIRouter

router = APIRouter(prefix="/devtools")

from . import genFakeData
