import os
import asyncio
from typing import Optional

from fastapi import Path, Body, Depends, Query

from . import router
from schemas.codes.codeContentSchema import CodeContentSchema
from schemas.operationResponseSchema import OpreationResponseSchema
from models.UserProjects import UserProjects
from models.ProjectCodes import ProjectCodes
from models.Users import Users
from models.TempProjects import TempProjects
from models.TempCodes import TempCodes
from depends.userInfoDependence import userInfo
from constants import ResopnseOperationResultType, PROJECT_BASE_DIR, TEMP_PROJECT_BASE_DIR, CodesType
from utils.codes.readCodes import readCodeFile
from utils.codes.writeCodes import writeCodeFile
from utils.codes.deleteCodes import deleteCodeFile as deleteCode


@router.get("/{cid:int}")
async def getCodeFileContent(
    user: Users | None = Depends(userInfo),
    pid: int = Path(),
    cid: int = Path(),
    temp: Optional[bool] = Query(default=False),
) -> CodeContentSchema | OpreationResponseSchema:
    """
    获取指定 cid 代码文件的内容
    """

    if temp == None or temp == False:
        targetProjectCode: ProjectCodes | None = await ProjectCodes.filter(cid=cid).first()  # type: ignore
    else:
        if user == None:
            return OpreationResponseSchema(
                code=403,
                result=ResopnseOperationResultType.FAIL,
                reason="user not login"
            )
            
        targetProjectCode: TempCodes | None = await TempCodes.filter(tcid=cid).first()

    if targetProjectCode == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="The code file could not be found"
        )
    

    if temp == None or temp == False:
        targetProject: UserProjects | None = await UserProjects.filter(pid=pid).first()  # type: ignore
    else:
        targetProject: TempProjects | None = await TempProjects.filter(tpid=pid).first()

    if targetProject == None:
        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="their has a sus thing that this code file exist but coundn't found its project"
        )


    try:
        eventloop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        codeFileName: str = f"{targetProjectCode.pathname}.{'vue' if targetProjectCode.type == CodesType.VUE else 'js'}"

        if temp == None or temp == False:
            codeFilePath: str = os.path.join(PROJECT_BASE_DIR, targetProject.name, codeFileName)
        else:
            codeFilePath: str = os.path.join(TEMP_PROJECT_BASE_DIR, targetProject.path, codeFileName)
        
        codeFileContent: str = await eventloop.run_in_executor(None, readCodeFile, codeFilePath)

    except Exception as e:
        print(e)

        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="error when reading code file"
        )
    
    if temp == None or temp == False:
        return CodeContentSchema(
            cid=targetProjectCode.cid,  # type: ignore
            pid=targetProject.pid,  # type: ignore
            name=targetProjectCode.name,
            content=codeFileContent,
            type= "vue" if targetProjectCode.type == CodesType.VUE else "js"
        )
    else:
        return CodeContentSchema(
            cid=targetProjectCode.tcid,
            pid=targetProject.tpid,
            name=targetProjectCode.name,
            content=codeFileContent,
            type= "vue" if targetProjectCode.type == CodesType.VUE else "js"
        )


@router.patch("/{cid:int}")
async def modifyCodeFileContent(
    user: Users | None = Depends(userInfo),
    pid: int = Path(),
    cid: int = Path(),
    content: str = Body(embed=True),
    temp: Optional[bool] = Body(embed=True, default= None),
):
    """
    修改指定 cid 代码文件中的内容
    用于只允许修改自己项目中的代码
    """

    # 检查用户是否登录
    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    

    # 检查是否存在此代码文件
    if temp == None or temp == False:
        targetProjectCode: ProjectCodes | None = await ProjectCodes.filter(cid=cid).first()  # type: ignore
    else:
        targetProjectCode: TempCodes | None = await TempCodes.filter(tcid=cid).first()

    if targetProjectCode == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="the code file could not be found"
        )


    # 检查此代码文件是否存在一个对应的项目
    if temp == None or temp == False:
        targetProject: UserProjects | None = await UserProjects.filter(pid=pid).first()  # type: ignore
    else:
        targetProject: TempProjects | None = await TempProjects.filter(tpid=pid).first()

    if targetProject == None:
        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="their has a sus thing that this code file exist but coundn't found its project"
        )
    

    # 检查用户修改的是否是自己的项目
    if temp == None or temp == False:
        userTargetProject: UserProjects | None = await targetProject.filter(uid=user.uid).first()  # type: ignore
    else:
        userTargetProject: TempProjects | None = await targetProject.filter(uid=user.uid).first()

    if userTargetProject == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="this project is not yours"
        )
    

    eventloop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    try:
        codeFileName: str = f"{targetProjectCode.pathname}.{'vue' if targetProjectCode.type == CodesType.VUE else 'js'}"

        if temp == None or temp == False:
            codeFilePath = os.path.join(PROJECT_BASE_DIR, targetProject.name, codeFileName)
        else:
            codeFilePath = os.path.join(TEMP_PROJECT_BASE_DIR, targetProject.path, codeFileName)

        await eventloop.run_in_executor(None, writeCodeFile, codeFilePath, content)
    except Exception as e:
        print(e)

        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="error when saving file"
        )
    
    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )


@router.delete("/{cid:int}")
async def deleteCodeFile(
    user: Users | None = Depends(userInfo),
    pid: int = Path(),
    cid: int = Path(),
    temp: Optional[bool] = Body(embed=True, default= None),
):
    # 检查用户是否登录
    if user == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="user not login"
        )
    
    # 检查是否存在此代码文件
    if temp == None or temp == False:
        targetProjectCode: ProjectCodes | None = await ProjectCodes.filter(cid=cid).first()  # type: ignore
    else:
        targetProjectCode: TempCodes | None = await TempCodes.filter(tcid=cid).first()

    if targetProjectCode == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="the code file could not be found"
        )
    

    # 检查此代码文件是否存在一个对应的项目
    if temp == None or temp == False:
        targetProject: UserProjects | None = await UserProjects.filter(pid=pid).first()  # type: ignore
    else:
        targetProject: TempProjects | None = await TempProjects.filter(tpid=pid).first()

    if targetProject == None:
        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="their has a sus thing that this code file exist but coundn't found its project"
        )


    # 检查用户修改的是否是自己的项目
    if temp == None or temp == False:
        userTargetProject: UserProjects | None = await targetProject.filter(uid=user.uid).first()  # type: ignore
    else:
        userTargetProject: TempProjects | None = await targetProject.filter(uid=user.uid).first()

    if userTargetProject == None:
        return OpreationResponseSchema(
            code=403,
            result=ResopnseOperationResultType.FAIL,
            reason="this project is not yours"
        )


    eventloop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    try:
        codeFileName: str = f"{targetProjectCode.pathname}.{'vue' if targetProjectCode.type == CodesType.VUE else 'js'}"

        if temp == None or temp == False:
            codeFilePath = os.path.join(PROJECT_BASE_DIR, targetProject.name, codeFileName)
        else:
            codeFilePath = os.path.join(TEMP_PROJECT_BASE_DIR, targetProject.path, codeFileName)

        await eventloop.run_in_executor(None, deleteCode, codeFilePath)

        await targetProjectCode.delete()
    except Exception as e:
        return OpreationResponseSchema(
            code=500,
            result=ResopnseOperationResultType.FAIL,
            reason="error when deleting file"
        )
    
    return OpreationResponseSchema(
        code=200,
        result=ResopnseOperationResultType.OK,
        reason=""
    )
