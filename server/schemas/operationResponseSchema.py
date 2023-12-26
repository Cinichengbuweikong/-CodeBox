from pydantic import BaseModel
from constants import ResopnseOperationResultType


class OpreationResponseSchema(BaseModel):
    """
    一般操作响应体格式
    """
    
    code: int
    """
    响应状态码
    """

    result: ResopnseOperationResultType
    """
    操作是否成功
    """

    reason: str
    """
    如果操作失败的话则这里是原因 否则是一个空字符串
    """
