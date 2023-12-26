from typing import List, Optional

from fastapi import Query

from . import router
from models.UserProjects import UserProjects
from schemas.projects.projectsInfoSchema import ProjectInfoSchema


@router.get("/")
async def searchProjects(
    q: str = Query(),
    page: Optional[int] = Query(default=1, gt=0)
):
    """
    根据给定的关键词搜索项目
    """

    perpage = 6
    """
    每页有多少项目
    """

    filteredProjects = await UserProjects.filter(projectname__contains=q).all()

    filtered: List[ProjectInfoSchema] = []

    for p in filteredProjects[(page-1)*perpage: page*perpage]:  # type: ignore
        filtered.append(ProjectInfoSchema(
            pid=str(p.pid),
            uid=str(p.uid),
            projectname=p.projectname,
            description=p.description,
            effectimg=p.effectimg
        ))

    return {
        "total": len(filteredProjects),
        "perpage": perpage,
        "page": page,
        "data": filtered
    }
