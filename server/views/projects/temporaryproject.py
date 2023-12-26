from typing import Optional
import asyncio
from typing import List

from fastapi import Body, Depends, Query

from . import router
from constants import TEMP_PROJECT_BASE_DIR, ProjectType, ResopnseOperationResultType, CodesType
from utils.projects.copyProjectsAsTemporaryProject import copyProjectsAsTemporaryProject
from utils.projects.copyTemporaryProjectAsProject import copyTemporaryProjectAsProject
from utils.projects.createProject import createProject
from utils.projects.deleteProject import removeProject
from models.TempProjects import TempProjects
from models.TempCodes import TempCodes
from models.Users import Users
from models.UserProjects import UserProjects
from models.ProjectCodes import ProjectCodes
from schemas.operationResponseSchema import OpreationResponseSchema
from schemas.projects.temporaryProjectInfoSchema import TemporaryProjectInfoSchema
from schemas.projects.getTemporaryProjectInfoResponseSchema import GetTemporaryProjectInfoSchema
from schemas.users.createProjectResponseSchema import CreateProjectResponseSchema
from depends.userInfoDependence import userInfo


@router.get("/temporaryproject")
async def getAllUsersTemporaryProject(
    user: Users | None = Depends(userInfo),
    tpid: Optional[int] = Query(default=None)
):
    """
    获取当前用户的所有临时项目
    """

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    
    if tpid == None:
        temporaryProjectDataList: List[TempProjects] = \
            await TempProjects.filter(uid=user.uid).all()
        
        if len(temporaryProjectDataList) == 0:
            return OpreationResponseSchema(
                code=404,
                result=ResopnseOperationResultType.FAIL,
                reason="project not found"
            )
        
        responseData: List[GetTemporaryProjectInfoSchema] = []

        for p in temporaryProjectDataList:
            responseData.append(GetTemporaryProjectInfoSchema(
                tpid=p.tpid, 
                uid=user.uid, 
                spid=p.spid, 
                name=p.name
            ))

        return responseData
    
    # tpid != None

    targetTemporaryProject: TempProjects | None = \
        await TempProjects.filter(uid=user.uid).filter(tpid=tpid).first()
    
    if targetTemporaryProject == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="project not found"
        )

    return GetTemporaryProjectInfoSchema(
        tpid=targetTemporaryProject.tpid,
        uid=user.uid,
        spid=targetTemporaryProject.spid,
        name=targetTemporaryProject.name
    )



@router.post("/temporaryproject")
async def createTemporayProject(
    user: Users | None = Depends(userInfo),
    pid: Optional[int] = Body(embed=True, default=None)
):
    """
    新建临时项目
    """

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    
    eventloop = asyncio.get_event_loop()


    if pid == None:
        # 如果 pid 是 none 的话 只需新建一个临时工程即可

        tempProjectFloderName, appFileName = await eventloop.run_in_executor(None, createProject, ProjectType.TEMP)
        
        newTempProject = TempProjects(
            uid=user.uid,
            path=tempProjectFloderName,
            name="我的临时项目"
        )

        await newTempProject.save()

        newTempProjectCode = TempCodes(
            tpid=newTempProject.tpid,
            name="App",
            pathname=appFileName,
            type=CodesType.VUE
        )

        await newTempProjectCode.save()
    else:
        # 如果 pid 不是 none  我们需要将 pid 指向的项目复制一份到临时文件夹

        targetProject: UserProjects | None = await UserProjects.filter(pid=pid).first()

        if targetProject == None:
            return OpreationResponseSchema(
                code=404,
                result=ResopnseOperationResultType.FAIL,
                reason="project not found"
            )

        try:
            newTempProjectName: str = await eventloop.run_in_executor(None, copyProjectsAsTemporaryProject, targetProject.name)

            newTempProject = TempProjects(
                uid=user.uid,
                pid=targetProject.pid,
                path=newTempProjectName,
                spid=targetProject.pid,
                name=f"my temporary project - {targetProject.projectname}"
            )

            await newTempProject.save()
        except Exception as e:
            print(e)

            return OpreationResponseSchema(
                code=500,
                result=ResopnseOperationResultType.FAIL,
                reason="error when creating temporary project"
            )

        targetProjectCodes: List[ProjectCodes] | None = await ProjectCodes.filter(pid=targetProject.pid).all()

        for c in targetProjectCodes:
            newTempProjectCode = TempCodes(
                tpid=newTempProject.tpid,
                name=c.name,
                pathname=c.pathname,
                type=c.type
            )

            await newTempProjectCode.save()
    

    return TemporaryProjectInfoSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason="",
        tpid=newTempProject.tpid
    )


@router.put("/temporaryproject")
async def saveTemporayProjectToNormalProject(
    user: Users | None = Depends(userInfo),
    tpid: int = Body(embed=True)
):
    # 检查用户是否登录
    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )


    # 检查项目是否存在 即使存在那也要检查这个项目是否是用户自己的
    targetTempProject: TempProjects | None = await TempProjects.filter(tpid=tpid).first()

    if targetTempProject == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="project not found"
        )
    
    userTargetTempProject: TempProjects | None = await targetTempProject.filter(uid=user.uid).first()

    if userTargetTempProject == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="this project isn't yours"
        )
    

    # 新建普通项目
    eventloop = asyncio.get_event_loop()

    newProjectFloderName = await eventloop.run_in_executor(None, copyTemporaryProjectAsProject, userTargetTempProject.path)
    
    newProject = UserProjects(
        uid=user.uid,
        projectname=userTargetTempProject.name,
        name=newProjectFloderName
    )

    await newProject.save()


    # 将临时项目的代码保存到普通项目中
    tempProjectCodes: List[TempCodes] | None = await TempCodes.filter(tpid=tpid).all()

    for c in tempProjectCodes:
        newProjectCode = ProjectCodes(
            pid=newProject.pid,
            name=c.name,
            pathname=c.pathname,
            type=c.type
        )

        await newProjectCode.save()

    
    # 删除临时项目
    await eventloop.run_in_executor(None, removeProject, str(targetTempProject.path), ProjectType.TEMP)
    await targetTempProject.delete()


    # 删除临时项目代码
    for c in tempProjectCodes:
        await c.delete()


    return CreateProjectResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason="",
        pid=newProject.pid
    )


@router.delete("/temporaryproject")
async def deleteTemporayProject(
    user: Users | None = Depends(userInfo),
    tpid: int = Body(embed=True)
):
    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    
    eventloop = asyncio.get_event_loop()

    targetTempProject: TempProjects | None = await TempProjects.filter(tpid=tpid).first()

    if targetTempProject == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="project not found"
        )
    
    userTargetTempProject: TempProjects | None = await targetTempProject.filter(uid=user.uid).first()

    if userTargetTempProject == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="this project isn't yours"
        )
    
    try:
        allTempCodes: List[TempCodes] | None = await TempCodes.filter(tpid=tpid).all()

        for c in allTempCodes:
            await c.delete()

        await targetTempProject.delete()

        await eventloop.run_in_executor(None, removeProject, str(targetTempProject.path), ProjectType.TEMP)
    except Exception as e:
        print(e)

        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="error when deleting project"
        )
    
    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )


