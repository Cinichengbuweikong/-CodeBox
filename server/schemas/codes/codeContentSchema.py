from pydantic import BaseModel


class CodeContentSchema(BaseModel):
    """
    代码内容响应模型
    """

    cid: int
    """
    代码文件的 id
    """

    pid: int
    """
    代码文件所属的项目的 id
    """

    name: str
    """
    代码文件的名字
    """

    content: str
    """
    代码内容
    """

    type: str
    """
    代码文件类型 取值 "vue" | "js"
    """
