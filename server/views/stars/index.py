from fastapi import Depends, Query

from . import router
from models.Users import Users
from models.UserStars import UserStars
from depends.userInfoDependence import userInfo
from schemas.operationResponseSchema import OpreationResponseSchema
from schemas.stars.starsResponseSchema import StarsResponseSchema
from constants import ResopnseOperationResultType


@router.get("/")
async def index(
    user: Users | None = Depends(userInfo),
    pid: str = Query(default=...)
):
    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    
    targetUserStars: UserStars | None = await UserStars.filter(uid=user.uid).filter(pid=pid).first()

    if targetUserStars != None:
        return StarsResponseSchema(
            code=200,
            result=ResopnseOperationResultType.OK,
            reason="",
            star=True
        )
    else:
        return StarsResponseSchema(
            code=200,
            result=ResopnseOperationResultType.OK,
            reason="",
            star=False
        )
