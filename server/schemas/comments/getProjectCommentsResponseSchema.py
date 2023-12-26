from pydantic import BaseModel


class GetProjectCommentsResponseSchema(BaseModel):
    """
    向客户端返回的项目评论信息的模型类
    """

    cid: int
    """
    评论 id
    """

    uid: int
    """
    评论用户 id
    """

    comment: str
    """
    评论内容
    """

    date: str
    """
    用户评论日期
    """

    like: int
    """
    赞数
    """

    youlike: bool
    """
    当前用户是否赞这个评论
    """
