from pydantic import BaseModel


class ProjectInfoSchema(BaseModel):
    """
    包含项目概要信息的模型类
    """

    pid: str
    """
    项目 id
    """

    uid: str
    """
    该项目所属的用户的 uid
    """

    projectname: str
    """
    用户名
    """

    description: str
    """
    用户头像链接
    """

    effectimg: str
    """
    效果图文件名
    """
