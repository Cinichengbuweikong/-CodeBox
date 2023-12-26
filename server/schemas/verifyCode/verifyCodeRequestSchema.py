from typing import Optional

from pydantic import BaseModel
from fastapi import Body


class VerifyCodeRequestSchema(BaseModel):
    """
    发送验证码请求体格式
    """
    
    email: Optional[str] = Body(default=None, regex=r"[\w]+(\.[\w]+)*@[\w]+(\.[\w])+")
    """
    用户邮箱
    """

    uid: Optional[int] = Body(default=None)
    """
    要接受验证码的用户的 uid 
    """
