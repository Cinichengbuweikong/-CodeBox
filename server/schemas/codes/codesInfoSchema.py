from pydantic import BaseModel

from constants import CodesType


class CodesInfoSchema(BaseModel):
    """
    代码文件信息模型
    """

    name: str
    """
    代码文件名
    """

    type: str
    """
    代码文件类型 取值 "vue" 或 "js"
    """
