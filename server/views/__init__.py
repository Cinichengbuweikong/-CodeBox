from fastapi import FastAPI, APIRouter

app = FastAPI()

server = APIRouter(prefix="/api")


from .user import router as userRouter
from .projects import router as projectsRouter
from .stars import router as starsRouter
from . import signup, sendVerifyCode, login, logout


server.include_router(userRouter)
server.include_router(projectsRouter)
server.include_router(starsRouter)


app.include_router(server)
