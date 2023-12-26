from typing import Dict, List, Optional
import asyncio
import os

from fastapi import Path, Body, Depends, Query

from . import router
from schemas.codes.codesInfoSchema import CodesInfoSchema
from schemas.operationResponseSchema import OpreationResponseSchema
from models.Users import Users
from models.ProjectCodes import ProjectCodes
from models.UserProjects import UserProjects
from models.TempProjects import TempProjects
from models.TempCodes import TempCodes
from constants import ResopnseOperationResultType, PROJECT_BASE_DIR, TEMP_PROJECT_BASE_DIR, CodesType
from depends.userInfoDependence import userInfo
from utils.codes.newCodes import newCodeFile as newCodeFileCreator



@router.get("/")
async def getCodeInfo(
    user: Users | None = Depends(userInfo),
    pid: int = Path(),
    temp: Optional[bool] = Query(default=False)
) -> Dict[str, Dict] | OpreationResponseSchema:
    """
    获取指定 pid 项目下的所有代码文件的信息
    """
    
    if temp == None or temp == False:
        targetProject: UserProjects | None = await UserProjects.filter(pid=pid).first()

        if targetProject == None:
            return OpreationResponseSchema(
                code=404,
                result=ResopnseOperationResultType.FAIL,
                reason="project not found"
            )
        
        allProjectCodes: List[ProjectCodes] | None = await ProjectCodes.filter(pid=targetProject.pid).all()

        projectCodes: Dict[str, Dict] = {}

        for c in allProjectCodes:
            projectCodes[str(c.cid)] = CodesInfoSchema(
                name=c.name,
                type= "vue" if c.type == 0 else "js"
            ).model_dump()
        
        return projectCodes
    
    # temp == True

    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    
    targetTempProject: TempProjects | None = await TempProjects.filter(tpid=pid).first()

    if targetTempProject == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="project not found"
        )
    
    allTempProjectCodes: List[TempCodes] | None = await TempCodes.filter(tpid=targetTempProject.tpid).all()

    tempProjectCodes: Dict[str, Dict] = {}

    for c in allTempProjectCodes:
        tempProjectCodes[str(c.tcid)] = CodesInfoSchema(
            name=c.name,
            type= "vue" if c.type == 0 else "js"
        ).model_dump()
    
    return tempProjectCodes


@router.post("/")
async def newCode(
    user: Users | None = Depends(userInfo),
    pid: int = Path(),
    name: str = Body(embed=True),
    type: str = Body(embed=True),
    temp: Optional[bool] = Body(embed=True, default= None),
):
    """
    新建代码文件 用户需要登录 同时用户只能在自己的项目中新建代码文件
    """

    if type != "vue" and type != "js":
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="unsupport file type"
        )
    
    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    

    if temp == None or temp == False:
        targetProject: UserProjects | None = await UserProjects.filter(uid=user.uid).filter(pid=pid).first()  # type: ignore
    else:
        targetProject: TempProjects | None = await TempProjects.filter(uid=user.uid).filter(tpid=pid).first()

    if targetProject == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user doesn't own this project"
        )
    

    if temp == None or temp == False:
        sameNameCodeFile: ProjectCodes | None = await ProjectCodes.filter(pid=pid).filter(name=name).first()  # type: ignore
    else:
        sameNameCodeFile: TempCodes | None = await TempCodes.filter(tpid=pid).filter(name=name).first()

    if sameNameCodeFile != None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="already has a same name file"
        )
    

    if type == "vue":
        fileType: CodesType = CodesType.VUE
    elif type == "js":
        fileType: CodesType = CodesType.JS
    
    if temp == None or temp == False:
        floderName: str = targetProject.name  # type: ignore
    else:
        floderName: str = targetProject.path

    if temp == None or temp == False:
        floderPath = os.path.join(PROJECT_BASE_DIR, floderName)
    else:
        floderPath = os.path.join(TEMP_PROJECT_BASE_DIR, floderName)
    
    eventloop = asyncio.get_event_loop()
    

    try:
        newCodeFileName = await eventloop.run_in_executor(None, newCodeFileCreator, floderPath, fileType)
    except Exception as e:
        print(e)

        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="error when creating file"
        )
    
    if temp == None or temp == False:
        newCodeFile = ProjectCodes(
            pid=targetProject.pid,  # type: ignore
            name=name,
            pathname=newCodeFileName,
            type=fileType
        )
    else:
        newCodeFile = TempCodes(
            tpid=targetProject.tpid,
            name=name,
            pathname=newCodeFileName,
            type=fileType
        )

    await newCodeFile.save()


    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )
