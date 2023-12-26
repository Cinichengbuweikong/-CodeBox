from typing import List

from fastapi import Depends, Body, Query

from . import router
from depends.userInfoDependence import userInfo
from models.Users import Users
from models.UserStars import UserStars
from models.UserProjects import UserProjects
from schemas.operationResponseSchema import OpreationResponseSchema
from schemas.users.userStarsResponseSchema import UserStarsResponseSchema
from constants import ResopnseOperationResultType


@router.get("/stars")
async def getStars(
    user: Users | None = Depends(userInfo),
):
    """
    获取给定 uid 的用户的所有收藏
    """

    if user == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="user not found"
        )
    
    allUserStars: List[UserStars] = await UserStars.filter(uid=user.uid).all()
    stars: List[UserStarsResponseSchema] = []

    for s in allUserStars:
        project: UserProjects | None = await UserProjects.filter(pid=s.pid).first()

        if project != None:
            stars.append(UserStarsResponseSchema(
                pid=str(project.pid),
                uid=str(project.uid),
                projectname=project.projectname,
                description=project.description,
                effectimg=project.effectimg
            ))
    
    return stars


@router.post("/stars")
async def addStars(
    user: Users | None = Depends(userInfo),
    pid: str = Body(embed=True)
):
    """
    新建收藏
    只能当前用户登录后再为当前用户创建收藏
    """

    if user == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    
    newStar: UserStars = UserStars(
        uid=user.uid,
        pid=int(pid)
    )

    await newStar.save()

    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )


@router.delete("/stars")
async def removeStars(
    user: Users | None = Depends(userInfo),
    pid: str = Body(embed=True)
):
    """
    删除收藏 只有用户登录了同时要删除的收藏存在于当前用户的收藏中才可以删除
    """

    if user == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    
    targetStar: UserStars | None = await UserStars.filter(pid=int(pid)).first()

    if targetStar == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="Users don't have this star"
        )
    
    await targetStar.delete()

    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )
