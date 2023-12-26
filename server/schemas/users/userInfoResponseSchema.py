from pydantic import BaseModel


class userInfoResponseSchema(BaseModel):
    """
    向客户端返回的用户信息的模型类
    """
    
    uid: str
    """
    用户 id
    """

    username: str
    """
    用户名
    """

    avatarurl: str
    """
    用户头像链接
    """

    coin: int
    """
    硬币数
    """

    description: str
    """
    用户自我介绍
    """

    email: str
    """
    用户的邮箱
    """
