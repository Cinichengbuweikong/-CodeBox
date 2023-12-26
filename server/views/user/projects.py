from typing import List, Optional
import asyncio
import uuid
import os

from fastapi import Depends, Body, Form, UploadFile, Query

from . import router
from models.Users import Users
from models.UserProjects import UserProjects
from models.ProjectCodes import ProjectCodes
from depends.userInfoDependence import userInfo
from schemas.operationResponseSchema import OpreationResponseSchema
from schemas.users.userProjectResponseSchema import UserInfoResponseSchema
from schemas.users.createProjectResponseSchema import CreateProjectResponseSchema
from constants import ResopnseOperationResultType, ProjectType, PROJECT_EFFECTIMG_DIR, CodesType
from utils.projects.createProject import createProject
from utils.projects.deleteProject import removeProject


@router.get("/projects")
async def getAllUsersProjects(
    uid: Optional[int] = Query(default=None)
):
    """
    获取给定用户所有的项目的信息
    """
    
    userAllProjects: List[UserProjects] = await UserProjects.filter(uid=uid).all()
    userAllProjectsInfo: List[UserInfoResponseSchema] = []

    for p in userAllProjects:
        userAllProjectsInfo.append(UserInfoResponseSchema(
            pid=str(p.pid),
            projectname=p.projectname,
            description=p.description,
            effectimg=p.effectimg
        ))

    return userAllProjectsInfo



@router.patch("/projects")
async def newProjects(
    user: Users | None = Depends(userInfo),
    projectname: str = Body(embed=True)
):
    """
    新建一个项目
    """

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="not login"
        )
    
    eventloop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    fut = eventloop.run_in_executor(None, createProject, ProjectType.NORMAL)

    flodername, projectAppFileName = await fut

    newproject = UserProjects(
        uid=user.uid,
        projectname=projectname,
        name=flodername
    )

    await newproject.save()

    newProjectCode = ProjectCodes(
        pid=newproject.pid,
        name="App",
        pathname=projectAppFileName,
        type=CodesType.VUE
    )

    await newProjectCode.save()

    return CreateProjectResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason="",
        pid=newproject.pid
    )


@router.post("/projects")
async def modifyProjectInfo(
    user: Users | None = Depends(userInfo),
    pid: str = Form(),
    projectname: Optional[str] = Form(default=None),
    description: Optional[str] = Form(default=None),
    effectimg: Optional[UploadFile] = None
):
    """
    修改项目信息
    """

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="not login"
        )
    
    targetProject: UserProjects | None = await UserProjects.filter(pid=int(pid)).first()

    if targetProject == None:
        return OpreationResponseSchema(
            code=402,
            result=ResopnseOperationResultType.FAIL,
            reason="project not found"
        )
    
    if projectname != None:
        targetProject.projectname = projectname

    if description != None:
        targetProject.description = description

    if effectimg != None and effectimg.filename != "":
        try:
            content: bytes = await effectimg.read()
            imgname: str = uuid.uuid1().hex

            if effectimg.content_type == "image/jpeg":
                imgname = f"{imgname}.jpg"
            elif effectimg.content_type == "image/png":
                imgname = f"{imgname}.png"
            elif effectimg.content_type == "image/gif":
                imgname = f"{imgname}.gif"
            else:
                return OpreationResponseSchema(
                    code=403,
                    result=ResopnseOperationResultType.FAIL,
                    reason="unsupported img type"
                )

            with open(os.path.join(PROJECT_EFFECTIMG_DIR, imgname), "wb") as file:
                file.write(content)

            targetProject.effectimg = imgname
        except:
            return OpreationResponseSchema(
                code=500,
                result=ResopnseOperationResultType.FAIL,
                reason="error when saving img file"
            )
        
    await targetProject.save()

    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )



@router.delete("/projects")
async def deleteProject(
    user: Users | None = Depends(userInfo),
    pid: str = Body(embed=True),
):
    """
    删除项目
    """

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="not login"
        )
    
    targetProject: UserProjects | None = await UserProjects.filter(pid=int(pid)).first()

    print(targetProject)

    if targetProject == None:
        return OpreationResponseSchema(
            code=402,
            result=ResopnseOperationResultType.FAIL,
            reason="project not found"
        )
    
    eventloop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    await eventloop.run_in_executor(None, removeProject, targetProject.name, ProjectType.NORMAL)
    
    await targetProject.delete()

    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )
