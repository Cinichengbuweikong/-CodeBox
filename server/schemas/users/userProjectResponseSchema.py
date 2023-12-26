from pydantic import BaseModel


class UserInfoResponseSchema(BaseModel):
    """
    向客户端返回的用户项目信息的模型类
    """
    
    pid: str
    """
    项目 id
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
