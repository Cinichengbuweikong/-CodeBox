from pydantic import BaseModel


class GetTemporaryProjectInfoSchema(BaseModel):
    """
    客户端需要的临时项目的信息的模型类
    """

    tpid: int
    """
    临时项目 id
    """

    uid: int
    """
    此项目拥有者的用户 id
    """

    spid: int | None
    """
    源项目 id
    """

    name: str
    """
    项目名
    """
