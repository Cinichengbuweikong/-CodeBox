from fastapi import Path

from . import router
from models.UserProjects import UserProjects
from schemas.projects.projectsInfoSchema import ProjectInfoSchema
from schemas.operationResponseSchema import OpreationResponseSchema
from constants import ResopnseOperationResultType


@router.get("/")
async def getProjectInfo(
    pid: int = Path()
):
    """
    获取指定 id 对应的项目的信息
    """
    
    targetProject: UserProjects | None = await UserProjects.filter(pid=pid).first()

    if targetProject == None:
        return OpreationResponseSchema(
            code=404,
            result=ResopnseOperationResultType.FAIL,
            reason="project not found"
        )

    return ProjectInfoSchema(
        pid=str(targetProject.pid),
        uid=str(targetProject.uid),
        projectname=targetProject.projectname,
        description=targetProject.description,
        effectimg=targetProject.effectimg
    )
