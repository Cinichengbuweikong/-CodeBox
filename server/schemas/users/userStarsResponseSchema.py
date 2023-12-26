from pydantic import BaseModel


class UserStarsResponseSchema(BaseModel):
    """
    向客户端返回的用户收藏信息的模型类
    """

    pid: str
    """
    项目 id
    """

    uid: str
    """
    该项目所属用户的 uid
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
